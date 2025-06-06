"""
Analytics functionality for the Document Management System.
"""
import logging
from sqlalchemy import func, desc, and_, extract, select, cast, Date, text
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from app.models import Document, Tag, DocumentTag
from calendar import monthrange
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for document analytics."""
    
    def __init__(self, db: Session):
        """Initialize the analytics service with a database session."""
        self.db = db
    
    async def get_document_count_by_type(self) -> List[Dict[str, Any]]:
        """Get document count grouped by document type.
        
        Returns:
            List of dictionaries with document_type and count
        """
        if hasattr(self.db, 'execute'):
            stmt = (
                select(Document.document_type, func.count(Document.id).label('count'))
                .group_by(Document.document_type)
            )
            res = await self.db.execute(stmt)
            results = res.all()
        else:
            results = self.db.query(
                Document.document_type,
                func.count(Document.id).label("count")
            ).group_by(Document.document_type).all()
        
        return [{"document_type": doc_type, "count": count} for doc_type, count in results]
    
    async def get_document_count_by_status(self) -> List[Dict[str, Any]]:
        """Get document count grouped by status.
        
        Returns:
            List of dictionaries with status and count
        """
        if hasattr(self.db, 'execute'):
            stmt = (
                select(Document.status, func.count(Document.id).label('count'))
                .group_by(Document.status)
            )
            res = await self.db.execute(stmt)
            results = res.all()
        else:
            results = self.db.query(
                Document.status,
                func.count(Document.id).label("count")
            ).group_by(Document.status).all()
        
        return [{"status": status, "count": count} for status, count in results]
    
    async def get_document_count_by_month(self, months: int = 6) -> List[Dict[str, Any]]:
        """Get document count by month for the last N months.
        
        Args:
            months: Number of months to include
            
        Returns:
            List of dictionaries with month, year, and count
        """
        today = datetime.utcnow()
        start_date = today - timedelta(days=30 * months)
        
        if hasattr(self.db, "execute"):
            # Async mode - For string date fields, we need to fetch and parse manually  
            stmt = select(Document)
            result = await self.db.execute(stmt)
            documents = result.scalars().all()
            
            # Group by year/month manually
            monthly_data = {}
            
            for doc in documents:
                # Use created_at if document_date is not available
                date_to_use = None
                
                if doc.document_date:
                    try:
                        # Parse document_date string
                        date_str = str(doc.document_date)
                        
                        # Try ISO format first
                        if re.match(r'^\d{4}-\d{2}-\d{2}', date_str):
                            date_to_use = datetime.strptime(date_str[:10], '%Y-%m-%d')
                        # Try European format
                        elif re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}', date_str):
                            parts = date_str.split('.')
                            if len(parts) >= 3:
                                date_to_use = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
                    except (ValueError, TypeError, IndexError):
                        pass
                
                # Fallback to created_at if document_date parsing failed
                if not date_to_use and doc.created_at:
                    date_to_use = doc.created_at
                
                if not date_to_use or date_to_use < start_date:
                    continue
                    
                year = date_to_use.year
                month = date_to_use.month
                key = f"{year}-{month:02d}"
                
                if key not in monthly_data:
                    monthly_data[key] = {
                        "year": year,
                        "month": month,
                        "month_name": date_to_use.strftime('%B'),
                        "count": 0
                    }
                
                monthly_data[key]["count"] += 1
            
            # Convert to list and sort
            results = list(monthly_data.values())
            results.sort(key=lambda x: (x["year"], x["month"]))
            
        else:
            # Sync mode fallback - this shouldn't be used in the current setup
            results = []
        
        return results
    
    async def get_invoice_amount_by_month(self, months: int = 6) -> List[Dict[str, Any]]:
        """Get total invoice amount by month for the last N months.
        
        Args:
            months: Number of months to include
            
        Returns:
            List of dictionaries with month, year, and total_amount
        """
        today = datetime.utcnow()
        start_date = today - timedelta(days=30 * months)
        
        if hasattr(self.db, "execute"):
            # Async mode - For string date fields, we need to fetch and parse manually
            stmt = select(Document).where(
                Document.document_type == 'invoice',
                Document.amount.isnot(None)
            )
            
            result = await self.db.execute(stmt)
            documents = result.scalars().all()
            
            # Group by year/month manually
            monthly_data = {}
            
            for doc in documents:
                if not doc.document_date:
                    continue
                    
                try:
                    # Parse date string (could be ISO format or European format)
                    date_str = str(doc.document_date)
                    
                    # Try ISO format first
                    if re.match(r'^\d{4}-\d{2}-\d{2}', date_str):
                        doc_date = datetime.strptime(date_str[:10], '%Y-%m-%d')
                    # Try European format
                    elif re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}', date_str):
                        parts = date_str.split('.')
                        if len(parts) >= 3:
                            doc_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
                    else:
                        continue
                        
                    # Check if within date range
                    if doc_date < start_date:
                        continue
                        
                    year = doc_date.year
                    month = doc_date.month
                    key = f"{year}-{month:02d}"
                    
                    if key not in monthly_data:
                        monthly_data[key] = {
                            "year": year,
                            "month": month,
                            "month_name": doc_date.strftime('%B'),
                            "total_amount": 0.0,
                            "count": 0
                        }
                    
                    monthly_data[key]["total_amount"] += float(doc.amount) if doc.amount else 0.0
                    monthly_data[key]["count"] += 1
                    
                except (ValueError, TypeError, IndexError) as e:
                    # Skip documents with invalid dates
                    continue
            
            # Convert to list and sort
            results = list(monthly_data.values())
            results.sort(key=lambda x: (x["year"], x["month"]))
            
        else:
            # Sync mode fallback - this shouldn't be used in the current setup
            results = []
        
        return results
    
    async def get_payment_status_summary(self) -> Dict[str, Any]:
        """Get summary counts + amounts for invoice payment status (async-aware)."""
        today = datetime.utcnow().date()

        async def _scalar(stmt):
            if hasattr(self.db, "execute"):
                res = await self.db.execute(stmt)
                return res.scalar() or 0
            return stmt.scalar()  # type: ignore – sync Session path

        if hasattr(self.db, "execute"):
            # Async mode – craft select() statements
            iso_due = Document.due_date.op('~')(r'^\\d{4}-\\d{2}-\\d{2}$')
            base = select(func.count(Document.id)).where(Document.document_type == "invoice")
            total_invoices = await _scalar(base)

            paid_invoices = await _scalar(
                base.where(Document.status == "paid")
            )
            unpaid_invoices = await _scalar(
                base.where(Document.status == "unpaid")
            )
            overdue_invoices = await _scalar(
                base.where(Document.status == "unpaid", iso_due, cast(Document.due_date, Date) < today)
            )

            # Amount aggregates
            amt_base = select(func.sum(Document.amount)).where(
                Document.document_type == "invoice", Document.amount.isnot(None)
            )
            total_amount = await _scalar(amt_base)
            paid_amount = await _scalar(amt_base.where(Document.status == "paid"))
            unpaid_amount = await _scalar(amt_base.where(Document.status == "unpaid"))
            overdue_amount = await _scalar(
                amt_base.where(Document.status == "unpaid", iso_due, cast(Document.due_date, Date) < today)
            )
        else:
            # Legacy sync Session
            iso_due_sync = Document.due_date.op('~')(r'^\\d{4}-\\d{2}-\\d{2}$')
            total_invoices = self.db.query(func.count(Document.id)).filter(Document.document_type == "invoice").scalar() or 0
            paid_invoices = self.db.query(func.count(Document.id)).filter(Document.document_type == "invoice", Document.status == "paid").scalar() or 0
            unpaid_invoices = self.db.query(func.count(Document.id)).filter(Document.document_type == "invoice", Document.status == "unpaid").scalar() or 0
            overdue_invoices = self.db.query(func.count(Document.id)).filter(Document.document_type == "invoice", Document.status == "unpaid", iso_due_sync, cast(Document.due_date, Date) < today).scalar() or 0

            total_amount = self.db.query(func.sum(Document.amount)).filter(Document.document_type == "invoice", Document.amount.isnot(None)).scalar() or 0
            paid_amount = self.db.query(func.sum(Document.amount)).filter(Document.document_type == "invoice", Document.status == "paid", Document.amount.isnot(None)).scalar() or 0
            unpaid_amount = self.db.query(func.sum(Document.amount)).filter(Document.document_type == "invoice", Document.status == "unpaid", Document.amount.isnot(None)).scalar() or 0
            overdue_amount = self.db.query(func.sum(Document.amount)).filter(Document.document_type == "invoice", Document.status == "unpaid", iso_due_sync, cast(Document.due_date, Date) < today, Document.amount.isnot(None)).scalar() or 0

        return {
            "total_invoices": total_invoices,
            "paid_invoices": paid_invoices,
            "unpaid_invoices": unpaid_invoices,
            "overdue_invoices": overdue_invoices,
            "total_amount": float(total_amount),
            "paid_amount": float(paid_amount),
            "unpaid_amount": float(unpaid_amount),
            "overdue_amount": float(overdue_amount),
            "paid_percentage": (paid_invoices / total_invoices * 100) if total_invoices else 0,
            "unpaid_percentage": (unpaid_invoices / total_invoices * 100) if total_invoices else 0,
            "overdue_percentage": (overdue_invoices / total_invoices * 100) if total_invoices else 0,
        }
    
    def get_upcoming_due_dates(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get documents with upcoming due dates.
        
        Args:
            days: Number of days ahead to check
            
        Returns:
            List of documents with upcoming due dates
        """
        today = datetime.utcnow().date()
        end_date = today + timedelta(days=days)
        
        documents = self.db.query(Document).filter(
            Document.due_date >= today,
            Document.due_date <= end_date,
            Document.status != 'paid'
        ).order_by(Document.due_date).all()
        
        result = []
        for doc in documents:
            days_until_due = (doc.due_date - today).days
            result.append({
                "id": doc.id,
                "title": doc.title,
                "sender": doc.sender,
                "due_date": doc.due_date.isoformat() if doc.due_date else None,
                "amount": float(doc.amount) if doc.amount else None,
                "document_type": doc.document_type,
                "days_until_due": days_until_due
            })
        
        return result
    
    def get_tag_distribution(self) -> List[Dict[str, Any]]:
        """Get document count by tag.
        
        Returns:
            List of dictionaries with tag name, color, and document count
        """
        results = self.db.query(
            Tag.name,
            Tag.color,
            func.count(DocumentTag.document_id).label("count")
        ).join(
            DocumentTag, Tag.id == DocumentTag.tag_id
        ).group_by(
            Tag.id
        ).order_by(
            desc("count")
        ).all()
        
        return [{"name": name, "color": color, "count": count} for name, color, count in results]
    
    def get_document_count_by_day_of_week(self) -> List[Dict[str, Any]]:
        """Get document count by day of week.
        
        Returns:
            List of dictionaries with day of week and count
        """
        results = self.db.query(
            extract('dow', Document.created_at).label('day_of_week'),
            func.count(Document.id).label('count')
        ).group_by(
            extract('dow', Document.created_at)
        ).order_by(
            extract('dow', Document.created_at)
        ).all()
        
        # Map day numbers to names (0=Sunday, 1=Monday, etc.)
        day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        
        return [{"day_of_week": day_names[int(dow)], "count": count} for dow, count in results]

    # ------------------------------------------------------------------
    # Compat helper methods expected by older FastAPI routes (async-style)
    # ------------------------------------------------------------------

    async def get_document_type_distribution(self, *_):
        """Async wrapper returning document count by type."""
        return await self.get_document_count_by_type()

    async def get_payment_status_distribution(self, *_):
        """Async wrapper returning document count by status."""
        return await self.get_document_count_by_status()

    async def get_monthly_document_count(self, year: int, *_):
        """Return monthly document counts for a specific year."""
        data = await self.get_document_count_by_month(months=24)  # Retrieve last 2 years
        return [item for item in data if item["year"] == year]

    async def get_monthly_invoice_amount(self, year: int, *_):
        """Return monthly invoice amounts for a specific year."""
        data = await self.get_invoice_amount_by_month(months=24)
        return [item for item in data if item["year"] == year]

    async def get_summary_metrics(self, *_):
        """Aggregate high-level KPIs used by dashboard."""
        return {
            "by_type": await self.get_document_count_by_type(),
            "by_status": await self.get_document_count_by_status(),
            "payment_summary": await self.get_payment_status_summary(),
        }

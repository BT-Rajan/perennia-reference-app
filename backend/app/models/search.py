"""Search provider implementations for ABC Enterprises reference application.

This module demonstrates how to implement SearchProviders for perennia-search,
registering different business resources that can be searched across the application.
"""

from perennia_search import SearchProvider, ProviderDocument


class CustomerSearchProvider(SearchProvider):
    """Search provider for customer records.
    
    Demonstrates indexing customer data (name, email, phone) for full-text search.
    In a real application, this would query your actual customer database.
    """

    def build_document(self, entity_id: str) -> ProviderDocument:
        """Build a searchable document from a customer entity.
        
        Args:
            entity_id: The customer ID to index
            
        Returns:
            ProviderDocument with title, content, and metadata
        """
        # In a real application, fetch from database:
        # customer = db.customers.get(entity_id)
        
        # Mock data for demonstration
        mock_customers = {
            "cust-001": {
                "name": "Acme Corporation",
                "email": "contact@acme.com",
                "phone": "+1-555-0100",
                "industry": "Manufacturing",
                "status": "active",
            },
            "cust-002": {
                "name": "Global Services Ltd",
                "email": "info@globalservices.com",
                "phone": "+1-555-0200",
                "industry": "Consulting",
                "status": "active",
            },
            "cust-003": {
                "name": "Tech Innovations Inc",
                "email": "hello@techinnovations.com",
                "phone": "+1-555-0300",
                "industry": "Software",
                "status": "inactive",
            },
        }
        
        customer = mock_customers.get(entity_id, {})
        
        return ProviderDocument(
            title=customer.get("name", "Unknown Customer"),
            content=" ".join([
                customer.get("name", ""),
                customer.get("email", ""),
                customer.get("phone", ""),
                customer.get("industry", ""),
            ]).strip(),
            metadata={
                "email": customer.get("email", ""),
                "phone": customer.get("phone", ""),
                "industry": customer.get("industry", ""),
                "status": customer.get("status", ""),
            },
        )

    def list_entity_ids(self) -> list[str]:
        """Return all customer IDs available for indexing.
        
        Returns:
            List of customer entity IDs
        """
        # In a real application: return db.customers.get_all_ids()
        return ["cust-001", "cust-002", "cust-003"]


class CompanySearchProvider(SearchProvider):
    """Search provider for company/partner records.
    
    Demonstrates indexing company metadata for searchable discovery.
    """

    def build_document(self, entity_id: str) -> ProviderDocument:
        """Build a searchable document from a company entity.
        
        Args:
            entity_id: The company ID to index
            
        Returns:
            ProviderDocument with title, content, and metadata
        """
        # Mock data for demonstration
        mock_companies = {
            "comp-001": {
                "name": "ABC Enterprises",
                "description": "Leading provider of enterprise solutions and business services",
                "headquarters": "New York, USA",
                "employees": 5000,
                "established": 2010,
            },
            "comp-002": {
                "name": "Northern Distribution",
                "description": "Supply chain and logistics optimization partner",
                "headquarters": "Toronto, Canada",
                "employees": 1200,
                "established": 2005,
            },
            "comp-003": {
                "name": "Pacific Trade Group",
                "description": "International trade and import-export specialist",
                "headquarters": "Singapore",
                "employees": 800,
                "established": 2015,
            },
        }
        
        company = mock_companies.get(entity_id, {})
        
        return ProviderDocument(
            title=company.get("name", "Unknown Company"),
            content=" ".join([
                company.get("name", ""),
                company.get("description", ""),
                company.get("headquarters", ""),
            ]).strip(),
            metadata={
                "headquarters": company.get("headquarters", ""),
                "employees": str(company.get("employees", "")),
                "established": str(company.get("established", "")),
            },
        )

    def list_entity_ids(self) -> list[str]:
        """Return all company IDs available for indexing.
        
        Returns:
            List of company entity IDs
        """
        # In a real application: return db.companies.get_all_ids()
        return ["comp-001", "comp-002", "comp-003"]


class DocumentSearchProvider(SearchProvider):
    """Search provider for business documents (contracts, agreements, etc.).
    
    Demonstrates integration with perennia-files for full-text search of document content.
    """

    def build_document(self, entity_id: str) -> ProviderDocument:
        """Build a searchable document from file metadata and extracted text.
        
        Args:
            entity_id: The document/file ID to index
            
        Returns:
            ProviderDocument with title, extracted content, and metadata
        """
        # Mock data for demonstration
        mock_documents = {
            "doc-001": {
                "filename": "Service Agreement 2024.pdf",
                "extracted_text": "This service agreement outlines the terms and conditions for professional services...",
                "document_type": "Service Agreement",
                "created_by": "user-123",
                "size_bytes": 256000,
            },
            "doc-002": {
                "filename": "Employee Handbook.docx",
                "extracted_text": "Welcome to ABC Enterprises. This handbook contains policies, procedures, and guidelines...",
                "document_type": "Policy",
                "created_by": "admin-001",
                "size_bytes": 512000,
            },
        }
        
        doc = mock_documents.get(entity_id, {})
        
        return ProviderDocument(
            title=doc.get("filename", "Unknown Document"),
            content=doc.get("extracted_text", ""),
            metadata={
                "type": doc.get("document_type", ""),
                "created_by": doc.get("created_by", ""),
                "size": str(doc.get("size_bytes", "")),
            },
        )

    def list_entity_ids(self) -> list[str]:
        """Return all document IDs available for indexing.
        
        Returns:
            List of document entity IDs
        """
        # In a real application: return db.files.get_all_ids()
        # or integrate with perennia_files.list_all_files()
        return ["doc-001", "doc-002"]

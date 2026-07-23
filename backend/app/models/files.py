"""File storage and handling models for ABC Enterprises reference application.

This module demonstrates how to integrate perennia-files for secure file uploads,
versioning, and optional AI processing of documents.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class FileMetadata(BaseModel):
    """Metadata for uploaded files."""
    
    id: str
    filename: str
    mime_type: str
    size_bytes: int
    version: int
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None
    is_deleted: bool = False


class FileUploadRequest(BaseModel):
    """Request model for file uploads."""
    
    filename: str
    description: Optional[str] = None
    tags: list[str] = []
    retain_original: bool = True  # Retain original file alongside any AI-processed versions


class FileVersionInfo(BaseModel):
    """Information about a specific file version."""
    
    version_number: int
    filename: str
    created_at: datetime
    created_by: str
    size_bytes: int
    is_current: bool


class FileAIProcessingRequest(BaseModel):
    """Request model for AI processing of files."""
    
    file_id: str
    operation: str  # 'summarize', 'extract', 'analyze', etc.
    parameters: Optional[dict] = None


class ContractDocument(BaseModel):
    """Domain model for contract documents stored via perennia-files."""
    
    file_id: str
    contract_name: str
    contract_type: str  # 'Service Agreement', 'NDA', 'Employment', etc.
    counterparty: str
    effective_date: datetime
    expiration_date: Optional[datetime] = None
    status: str  # 'draft', 'signed', 'executed', 'expired'
    stored_by: str
    extracted_terms: Optional[dict] = None  # AI-extracted key terms


class PolicyDocument(BaseModel):
    """Domain model for policy documents stored via perennia-files."""
    
    file_id: str
    policy_name: str
    policy_type: str  # 'HR', 'Security', 'Financial', etc.
    version: str
    effective_date: datetime
    status: str  # 'active', 'draft', 'archived'
    stored_by: str
    extracted_summary: Optional[str] = None  # AI-generated summary


class FileStorageManager:
    """Manager class for demonstrating file storage operations with perennia-files.
    
    This class shows how to organize file operations for different document types
    while integrating with perennia-files for secure storage and versioning.
    """

    def __init__(self):
        """Initialize the file storage manager.
        
        In a real application, this would be initialized with a PerenniaFiles instance:
        
            from perennia_files import PerenniaFiles, FilesConfig, DatabaseConfig
            
            config = FilesConfig(
                storage_path="/var/lib/app/files",
                signing_secret=os.environ["FILES_SIGNING_SECRET"],
                database=DatabaseConfig(host="...", user="...", password="...", database="..."),
                max_upload_size=50 * 1024 * 1024,
                encryption_enabled=True,
                ai_enabled=True,
                ai_provider=CustomAIProvider(),
            )
            self.files = PerenniaFiles(config)
        """
        pass

    def upload_contract(
        self,
        filename: str,
        data: bytes,
        contract_type: str,
        counterparty: str,
        effective_date: datetime,
        created_by: str,
    ) -> ContractDocument:
        """Upload and register a contract document.
        
        Args:
            filename: Name of the contract file
            data: Binary file content
            contract_type: Type of contract (Service Agreement, NDA, etc.)
            counterparty: Name of the counterparty
            effective_date: Date contract becomes effective
            created_by: Subject ID of uploader
            
        Returns:
            ContractDocument with file reference and metadata
            
        Example:
            contract = storage_manager.upload_contract(
                filename="acme_agreement.pdf",
                data=file_data,
                contract_type="Service Agreement",
                counterparty="Acme Corp",
                effective_date=datetime(2024, 1, 1),
                created_by="user-123",
            )
        """
        # In real implementation:
        # logical_file = self.files.upload(filename, data, created_by=created_by)
        # db.contracts.create(
        #     file_id=logical_file.id,
        #     contract_type=contract_type,
        #     counterparty=counterparty,
        #     effective_date=effective_date,
        #     status="draft",
        # )
        pass

    def upload_policy(
        self,
        filename: str,
        data: bytes,
        policy_type: str,
        policy_name: str,
        effective_date: datetime,
        created_by: str,
    ) -> PolicyDocument:
        """Upload and register a policy document.
        
        Args:
            filename: Name of the policy file
            data: Binary file content
            policy_type: Type of policy (HR, Security, etc.)
            policy_name: Name/title of the policy
            effective_date: Date policy becomes effective
            created_by: Subject ID of uploader
            
        Returns:
            PolicyDocument with file reference and metadata
        """
        # In real implementation:
        # logical_file = self.files.upload(filename, data, created_by=created_by)
        # if config.ai_enabled:
        #     extracted_summary = self.files.summarize(logical_file.id)
        # db.policies.create(
        #     file_id=logical_file.id,
        #     policy_type=policy_type,
        #     policy_name=policy_name,
        #     effective_date=effective_date,
        #     extracted_summary=extracted_summary if config.ai_enabled else None,
        # )
        pass

    def create_version(
        self,
        file_id: str,
        new_filename: str,
        data: bytes,
        created_by: str,
        change_description: Optional[str] = None,
    ) -> FileVersionInfo:
        """Create a new version of an existing file.
        
        Args:
            file_id: ID of the file to version
            new_filename: Filename for the new version
            data: Binary content of new version
            created_by: Subject ID creating the version
            change_description: Optional description of changes
            
        Returns:
            FileVersionInfo describing the new version
            
        Example:
            new_version = storage_manager.create_version(
                file_id="file-123",
                new_filename="agreement_v2.pdf",
                data=updated_content,
                created_by="user-123",
                change_description="Updated termination clause per legal review",
            )
        """
        # In real implementation:
        # version, meta = self.files.create_version(
        #     file_id,
        #     new_filename,
        #     data,
        #     created_by=created_by,
        # )
        # if change_description:
        #     db.file_versions.log_change(file_id, version, change_description)
        pass

    def download_file(self, file_id: str) -> tuple[str, bytes]:
        """Download the current version of a file.
        
        Args:
            file_id: ID of the file to download
            
        Returns:
            Tuple of (filename, file_data)
            
        Example:
            filename, data = storage_manager.download_file("file-123")
        """
        # In real implementation:
        # version, data = self.files.download(file_id)
        # return (version.filename, data)
        pass

    def list_versions(self, file_id: str) -> list[FileVersionInfo]:
        """List all versions of a file.
        
        Args:
            file_id: ID of the file
            
        Returns:
            List of FileVersionInfo objects
        """
        # In real implementation:
        # versions = db.file_versions.by_file_id(file_id)
        # return [FileVersionInfo(...) for v in versions]
        pass

    def soft_delete(self, file_id: str, deleted_by: str) -> None:
        """Soft-delete a file (mark as deleted but retain data).
        
        Args:
            file_id: ID of file to delete
            deleted_by: Subject ID requesting deletion
        """
        # In real implementation:
        # self.files.delete(file_id, deleted_by=deleted_by)
        pass

    def restore_file(self, file_id: str) -> None:
        """Restore a soft-deleted file.
        
        Args:
            file_id: ID of file to restore
        """
        # In real implementation:
        # self.files.restore(file_id)
        pass

    def ask_document(self, file_id: str, question: str) -> str:
        """Ask an AI question about document content (requires ai_enabled=True).
        
        Args:
            file_id: ID of the document
            question: Question to ask about the document
            
        Returns:
            AI-generated answer
            
        Example:
            answer = storage_manager.ask_document(
                file_id="contract-001",
                question="What is the termination clause?",
            )
        """
        # In real implementation:
        # return self.files.ask(file_id, question)
        pass

    def summarize_document(self, file_id: str) -> str:
        """Generate an AI summary of a document (requires ai_enabled=True).
        
        Args:
            file_id: ID of the document
            
        Returns:
            AI-generated summary
        """
        # In real implementation:
        # return self.files.summarize(file_id)
        pass

    def generate_content(self, file_id: str, prompt: str) -> str:
        """Generate new content based on document context (requires ai_enabled=True).
        
        Args:
            file_id: ID of the source document
            prompt: Prompt for generation (e.g., "Write a client-friendly summary")
            
        Returns:
            AI-generated content
        """
        # In real implementation:
        # return self.files.generate(file_id, prompt)
        pass

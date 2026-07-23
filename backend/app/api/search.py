"""Search API endpoints for ABC Enterprises reference application.

Demonstrates how to expose perennia-search functionality via FastAPI,
including model registration, indexing, and searching across business resources.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from perennia_access import AuthenticatedIdentity

from app.deps import access, get_current_identity
from app.permissions.definitions import SEARCH_ACCESS, SEARCH_MANAGE
from app.models.search import CustomerSearchProvider, CompanySearchProvider, DocumentSearchProvider

router = APIRouter(prefix="/api/search", tags=["search"])


# --- Request/Response Models ---


class SearchResult(BaseModel):
    """A single search result."""
    
    resource: str  # 'customer', 'company', 'document', etc.
    entity_id: str
    title: str
    score: float  # Relevance score from full-text search
    metadata: dict


class SearchResponse(BaseModel):
    """Response from search endpoint."""
    
    query: str
    results: list[SearchResult]
    total: int


class ResourceRegistration(BaseModel):
    """Resource registration info."""
    
    resource_name: str
    description: str
    indexed: bool
    entity_count: int


class IndexingStatus(BaseModel):
    """Status of indexing operations."""
    
    resource: str
    entity_id: str
    status: str  # 'indexed', 'pending', 'failed'
    message: str


# --- Endpoints ---


@router.get("/query", response_model=SearchResponse)
def search_query(
    q: str = Query(..., min_length=1, description="Search query keyword"),
    resource_filter: str | None = Query(None, description="Filter by resource type (optional)"),
    limit: int = Query(20, ge=1, le=100),
    identity: AuthenticatedIdentity = Depends(get_current_identity),
):
    """Execute a search query across indexed resources.
    
    Searches all registered and indexed resources for matching keywords.
    Results are ranked by relevance score.
    
    Args:
        q: Search query (required)
        resource_filter: Optionally filter results to specific resource type
        limit: Maximum results to return (default 20, max 100)
        identity: Current authenticated identity (used for authorization)
        
    Returns:
        SearchResponse with matched results
        
    Raises:
        HTTPException: 403 if user lacks search.execute permission
        HTTPException: 400 if query is invalid
        
    Example:
        GET /api/search/query?q=acme&limit=10
        GET /api/search/query?q=service+agreement&resource_filter=document
    """
    access.require(identity, SEARCH_ACCESS)
    
    # In real implementation:
    # from perennia_search import SearchQuery
    # results = search_engine.search(SearchQuery(keyword=q, resource_filter=resource_filter))
    # return SearchResponse(
    #     query=q,
    #     results=[
    #         SearchResult(
    #             resource=r.resource,
    #             entity_id=r.entity_id,
    #             title=r.title,
    #             score=r.score,
    #             metadata=r.metadata,
    #         )
    #         for r in results
    #     ],
    #     total=len(results),
    # )
    
    return SearchResponse(
        query=q,
        results=[],
        total=0,
    )


@router.get("/resources", response_model=list[ResourceRegistration])
def list_resources(
    identity: AuthenticatedIdentity = Depends(get_current_identity),
):
    """List all registered search resources.
    
    Returns information about each resource provider including:
    - Resource name and description
    - Whether it's currently indexed
    - Number of indexed entities
    
    Args:
        identity: Current authenticated identity
        
    Returns:
        List of ResourceRegistration objects
        
    Raises:
        HTTPException: 403 if user lacks search.manage permission
    """
    access.require(identity, SEARCH_MANAGE)
    
    # In real implementation:
    # resources = [
    #     ResourceRegistration(
    #         resource_name="customer",
    #         description="Customer records",
    #         indexed=True,
    #         entity_count=count_indexed_entities("customer"),
    #     )
    #     for resource in search_engine.list_registered_resources()
    # ]
    # return resources
    
    return [
        ResourceRegistration(
            resource_name="customer",
            description="Customer records",
            indexed=True,
            entity_count=3,
        ),
        ResourceRegistration(
            resource_name="company",
            description="Company/partner records",
            indexed=True,
            entity_count=3,
        ),
        ResourceRegistration(
            resource_name="document",
            description="Business documents (contracts, policies, etc.)",
            indexed=True,
            entity_count=2,
        ),
    ]


@router.post("/index/{resource}/{entity_id}")
def index_entity(
    resource: str,
    entity_id: str,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
) -> IndexingStatus:
    """Index a specific entity from a registered resource.
    
    Indexes a single entity (customer, company, document, etc.) for search.
    Use this when creating, updating, or reindexing individual records.
    
    Args:
        resource: Resource type name (customer, company, document, etc.)
        entity_id: ID of entity to index
        identity: Current authenticated identity
        
    Returns:
        IndexingStatus indicating success or failure
        
    Raises:
        HTTPException: 403 if user lacks search.manage permission
        HTTPException: 404 if resource type or entity not found
        
    Example:
        POST /api/search/index/customer/cust-123
        POST /api/search/index/document/doc-001
    """
    access.require(identity, SEARCH_MANAGE)
    
    # Validate resource type
    valid_resources = {"customer": CustomerSearchProvider(), "company": CompanySearchProvider(), "document": DocumentSearchProvider()}
    if resource not in valid_resources:
        raise HTTPException(status_code=404, detail=f"Resource type '{resource}' not found")
    
    # In real implementation:
    # provider = valid_resources[resource]
    # if entity_id not in provider.list_entity_ids():
    #     raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found in resource {resource}")
    # search_engine.index(resource, entity_id=entity_id)
    
    return IndexingStatus(
        resource=resource,
        entity_id=entity_id,
        status="indexed",
        message=f"Successfully indexed {entity_id}",
    )


@router.post("/rebuild/{resource}")
def rebuild_resource_index(
    resource: str,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
):
    """Rebuild the search index for an entire resource.
    
    Reindexes all entities for a resource type. This is an admin operation
    typically run during maintenance or after data migrations.
    
    Args:
        resource: Resource type to rebuild
        identity: Current authenticated identity
        
    Returns:
        Status message indicating rebuild completion
        
    Raises:
        HTTPException: 403 if user lacks search.manage permission
        HTTPException: 404 if resource not found
        
    Example:
        POST /api/search/rebuild/customer
    """
    access.require(identity, SEARCH_MANAGE)
    
    # Validate resource
    valid_resources = {"customer", "company", "document"}
    if resource not in valid_resources:
        raise HTTPException(status_code=404, detail=f"Resource type '{resource}' not found")
    
    # In real implementation:
    # search_engine.rebuild(resource)
    
    return {
        "status": "rebuilding",
        "resource": resource,
        "message": f"Started rebuilding index for resource '{resource}'",
    }


@router.post("/suggest")
def suggest(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    identity: AuthenticatedIdentity = Depends(get_current_identity),
):
    """Get search suggestions/autocomplete for a partial query.
    
    Returns keyword suggestions based on indexed content and search history.
    Useful for implementing search-as-you-type UI experiences.
    
    Args:
        q: Partial query for suggestions
        limit: Maximum suggestions to return
        identity: Current authenticated identity
        
    Returns:
        List of suggestion strings
        
    Example:
        GET /api/search/suggest?q=acm&limit=5
        Response: ["acme", "acme corporation", "acme supply"]
    """
    access.require(identity, SEARCH_ACCESS)
    
    # In real implementation:
    # suggestions = search_engine.suggest(q, limit=limit)
    # return {"suggestions": suggestions}
    
    return {
        "suggestions": [],
    }

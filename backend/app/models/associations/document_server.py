from sqlalchemy import BigInteger, ForeignKey, Table, Column

from app.core.database import Base

document_servers = Table(
    'document_servers',
    Base.metadata,
    Column(
        'document_id',
        BigInteger,
        ForeignKey('infrastructure_documents.id', ondelete='CASCADE'),
        primary_key=True
    ),

    Column(
        'server_id',
        BigInteger,
        ForeignKey('servers.id', ondelete='CASCADE'),
        primary_key = True
    )
)
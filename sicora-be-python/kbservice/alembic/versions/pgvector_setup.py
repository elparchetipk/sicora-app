"""Enable pgvector extension and create vector indexes

Revision ID: pgvector_setup
Revises: d2d3ebb2929d
Create Date: 2025-06-14 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = 'pgvector_setup'
down_revision = 'd2d3ebb2929d'
branch_labels = None
depends_on = None


def is_postgresql():
    """Check if we're using PostgreSQL."""
    bind = op.get_bind()
    return bind.dialect.name == 'postgresql'


def upgrade() -> None:
    """Enable pgvector extension and create vector indexes for PostgreSQL."""
    if not is_postgresql():
        print("⚠️ Skipping pgvector setup - not using PostgreSQL")
        return
    
    # Enable pgvector extension
    try:
        op.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        print("✅ pgvector extension enabled")
    except Exception as e:
        print(f"⚠️ Could not enable pgvector extension: {e}")
        return
    
    # Alter embedding column to use vector type
    try:
        # First, check if column exists and has data
        connection = op.get_bind()
        result = connection.execute(text("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_name = 'knowledge_items' AND column_name = 'embedding'
        """))
        
        row = result.fetchone()
        if row and row[0] > 0:
            # Drop existing column if it exists (will be recreated with vector type)
            op.drop_column('knowledge_items', 'embedding')
        
        # Add embedding column with vector type
        op.add_column('knowledge_items', 
                     sa.Column('embedding', 
                              sa.String(),  # This will be overridden by pgvector
                              nullable=True))
        
        # Now alter the column to use vector type
        op.execute(text("""
            ALTER TABLE knowledge_items 
            ALTER COLUMN embedding TYPE vector(1536) 
            USING embedding::vector(1536)
        """))
        
        print("✅ Embedding column configured for pgvector")
        
    except Exception as e:
        print(f"⚠️ Could not configure embedding column: {e}")
    
    # Create vector indexes
    try:
        # HNSW index for fast approximate similarity search
        op.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_knowledge_items_embedding_hnsw
            ON knowledge_items 
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64)
        """))
        
        # IVFFlat index as alternative
        op.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_knowledge_items_embedding_ivfflat
            ON knowledge_items 
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
        """))
        
        print("✅ Vector indexes created")
        
    except Exception as e:
        print(f"⚠️ Could not create vector indexes: {e}")


def downgrade() -> None:
    """Remove pgvector indexes and revert to JSON embedding."""
    if not is_postgresql():
        return
    
    # Drop vector indexes
    try:
        op.drop_index('idx_knowledge_items_embedding_hnsw', 'knowledge_items')
        op.drop_index('idx_knowledge_items_embedding_ivfflat', 'knowledge_items')
        print("✅ Vector indexes dropped")
    except Exception as e:
        print(f"⚠️ Could not drop vector indexes: {e}")
    
    # Revert embedding column to JSON
    try:
        op.execute(text("""
            ALTER TABLE knowledge_items 
            ALTER COLUMN embedding TYPE json 
            USING embedding::text::json
        """))
        print("✅ Embedding column reverted to JSON")
    except Exception as e:
        print(f"⚠️ Could not revert embedding column: {e}")
    
    # Note: We don't drop the pgvector extension as it might be used by other applications

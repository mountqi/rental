"""empty message

Revision ID: 49604deaa619
Revises: None
Create Date: 2016-05-19 17:49:46.194034

"""

# revision identifiers, used by Alembic.
revision = '49604deaa619'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agencies',
    sa.Column('agency_id', sa.Integer(), nullable=False),
    sa.Column('corp_name', sa.String(length=64), nullable=True),
    sa.Column('corp_license_no', sa.String(length=64), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('sub_account_no', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('agency_id'),
    sa.UniqueConstraint('corp_name')
    )
    op.create_table('cities',
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('city_no', sa.String(length=8), nullable=True),
    sa.Column('city_name', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('city_id'),
    sa.UniqueConstraint('city_name'),
    sa.UniqueConstraint('city_no')
    )
    op.create_table('fees',
    sa.Column('fee_id', sa.Integer(), nullable=False),
    sa.Column('fee_name', sa.String(length=32), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('time_length', sa.Integer(), nullable=True),
    sa.Column('time_length_type', sa.Integer(), nullable=True),
    sa.Column('tickets_no', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('fee_id'),
    sa.UniqueConstraint('fee_name')
    )
    op.create_table('property_sources',
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('source_name', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('source_id')
    )
    op.create_table('property_types',
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('type_name', sa.String(length=8), nullable=True),
    sa.PrimaryKeyConstraint('type_id')
    )
    op.create_table('role_groups',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.Column('remark', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('role_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('areas',
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('area_name', sa.String(length=16), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['cities.city_id'], ),
    sa.PrimaryKeyConstraint('area_id'),
    sa.UniqueConstraint('area_name')
    )
    op.create_table('districts',
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.Column('district_name', sa.String(length=16), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['cities.city_id'], ),
    sa.PrimaryKeyConstraint('district_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('login_name', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('phone_no', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('id_card_no', sa.String(length=20), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('user_type', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('agency_id', sa.Integer(), nullable=True),
    sa.Column('remark', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['agency_id'], ['agencies.agency_id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role_groups.role_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_login_name'), 'users', ['login_name'], unique=True)
    op.create_table('estates',
    sa.Column('estate_id', sa.Integer(), nullable=False),
    sa.Column('estate_name', sa.String(length=32), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('district_id', sa.Integer(), nullable=True),
    sa.Column('area_id', sa.Integer(), nullable=True),
    sa.Column('english_name', sa.String(length=64), nullable=True),
    sa.Column('zhpy', sa.String(length=16), nullable=True),
    sa.Column('complete_year', sa.String(length=8), nullable=True),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.Column('developer', sa.String(length=32), nullable=True),
    sa.Column('mgt_company', sa.String(length=32), nullable=True),
    sa.Column('mgt_fee', sa.Integer(), nullable=True),
    sa.Column('total_sqare', sa.Float(), nullable=True),
    sa.Column('total_houses', sa.Integer(), nullable=True),
    sa.Column('floor_area_ratio', sa.Float(), nullable=True),
    sa.Column('parking_no', sa.Integer(), nullable=True),
    sa.Column('green_rate', sa.Float(), nullable=True),
    sa.Column('introduction', sa.String(length=256), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['areas.area_id'], ),
    sa.ForeignKeyConstraint(['city_id'], ['cities.city_id'], ),
    sa.ForeignKeyConstraint(['district_id'], ['districts.district_id'], ),
    sa.PrimaryKeyConstraint('estate_id')
    )
    op.create_table('fee_records',
    sa.Column('fee_record_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('collector_id', sa.Integer(), nullable=True),
    sa.Column('fee_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('expire_time', sa.DateTime(), nullable=True),
    sa.Column('charge_time', sa.DateTime(), nullable=True),
    sa.Column('is_valid', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['collector_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['fee_id'], ['fees.fee_id'], ),
    sa.PrimaryKeyConstraint('fee_record_id')
    )
    op.create_table('properties',
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('district_id', sa.Integer(), nullable=True),
    sa.Column('estate_id', sa.Integer(), nullable=True),
    sa.Column('area_id', sa.Integer(), nullable=True),
    sa.Column('build_no', sa.String(length=16), nullable=True),
    sa.Column('floor', sa.Integer(), nullable=True),
    sa.Column('floor_all', sa.Integer(), nullable=True),
    sa.Column('room_no', sa.String(length=16), nullable=True),
    sa.Column('count_f', sa.Integer(), nullable=True),
    sa.Column('count_t', sa.Integer(), nullable=True),
    sa.Column('count_w', sa.Integer(), nullable=True),
    sa.Column('count_y', sa.Integer(), nullable=True),
    sa.Column('property_type', sa.Integer(), nullable=True),
    sa.Column('property_direction', sa.String(length=8), nullable=True),
    sa.Column('square', sa.Float(), nullable=True),
    sa.Column('owner_name', sa.String(length=16), nullable=True),
    sa.Column('contact_name', sa.String(length=16), nullable=True),
    sa.Column('contact_tel', sa.String(length=32), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('furniture', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('valid_time', sa.DateTime(), nullable=True),
    sa.Column('trust_grade', sa.Integer(), nullable=True),
    sa.Column('rent_price', sa.Float(), nullable=True),
    sa.Column('mgt_price', sa.Float(), nullable=True),
    sa.Column('reg_user_id', sa.Integer(), nullable=True),
    sa.Column('reg_time', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('longitude', sa.String(length=24), nullable=True),
    sa.Column('latitude', sa.String(length=24), nullable=True),
    sa.Column('source', sa.String(length=16), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['areas.area_id'], ),
    sa.ForeignKeyConstraint(['city_id'], ['cities.city_id'], ),
    sa.ForeignKeyConstraint(['district_id'], ['districts.district_id'], ),
    sa.ForeignKeyConstraint(['estate_id'], ['estates.estate_id'], ),
    sa.ForeignKeyConstraint(['reg_user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('property_id')
    )
    op.create_table('follows',
    sa.Column('follow_id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('follow_time', sa.DateTime(), nullable=True),
    sa.Column('follow_user_id', sa.Integer(), nullable=True),
    sa.Column('follow_content', sa.String(length=128), nullable=True),
    sa.Column('alert_time', sa.DateTime(), nullable=True),
    sa.Column('alert_user_id', sa.Integer(), nullable=True),
    sa.Column('alert_content', sa.String(length=128), nullable=True),
    sa.Column('process_time', sa.DateTime(), nullable=True),
    sa.Column('process_user_id', sa.Integer(), nullable=True),
    sa.Column('process_content', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['alert_user_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['follow_user_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['process_user_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['property_id'], ['properties.property_id'], ),
    sa.PrimaryKeyConstraint('follow_id')
    )
    op.create_table('images',
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('file_name', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.property_id'], ),
    sa.PrimaryKeyConstraint('image_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    op.drop_table('follows')
    op.drop_table('properties')
    op.drop_table('fee_records')
    op.drop_table('estates')
    op.drop_index(op.f('ix_users_login_name'), table_name='users')
    op.drop_table('users')
    op.drop_table('districts')
    op.drop_table('areas')
    op.drop_table('role_groups')
    op.drop_table('property_types')
    op.drop_table('property_sources')
    op.drop_table('fees')
    op.drop_table('cities')
    op.drop_table('agencies')
    ### end Alembic commands ###

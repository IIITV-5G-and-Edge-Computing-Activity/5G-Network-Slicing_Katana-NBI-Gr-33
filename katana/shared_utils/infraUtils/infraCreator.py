from katana.shared_utils.vimUtils.openstackUtils import Openstack
from katana.shared_utils.vimUtils.opennebulaUtils import Opennebula

class InfrastructureCreator:
    def __init__(self, vim_type):
        self.vim_type = vim_type
    
    def create_infrastructure(self, slice_data):
        """Creates required infrastructure for a network slice"""
        
        # Create tenant details
        tenant_name = f"slice_{slice_data['_id']}"
        tenant_desc = f"Infrastructure for slice {slice_data['slice_name']}"
        tenant_user = f"slice_user_{slice_data['_id']}"
        tenant_pass = "secure_password"  # Should be generated securely
        
        if self.vim_type == "openstack":
            vim = Openstack(
                uuid=slice_data['_id'],
                auth_url=slice_data['vim_url'], 
                project_name=tenant_name,
                username=tenant_user,
                password=tenant_pass
            )
            
            # Create OpenStack resources
            return vim.create_slice_prerequisites(
                tenant_project_name=tenant_name,
                tenant_project_description=tenant_desc, 
                tenant_project_user=tenant_user,
                tenant_project_password=tenant_pass,
                slice_uuid=slice_data['_id'],
                quotas=slice_data.get('quotas')
            )
            
        elif self.vim_type == "opennebula":
            vim = Opennebula(
                uuid=slice_data['_id'],
                auth_url=slice_data['vim_url'],
                project_name=tenant_name,
                username=tenant_user, 
                password=tenant_pass
            )
            
            # Create OpenNebula resources
            return vim.create_slice_prerequisites(
                tenant_project_name=tenant_name,
                tenant_project_description=tenant_desc,
                tenant_project_user=tenant_user,
                tenant_project_password=tenant_pass,
                slice_uuid=slice_data['_id']
            )
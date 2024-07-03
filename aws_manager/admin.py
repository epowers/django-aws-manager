from django.contrib import admin
from django.contrib import messages

from django.utils.html import format_html
import boto3

class AWSServerAdmin(admin.ModelAdmin):

    list_display = ('name', 'description', 'user_name','aws_region')

    state = None
    public_dns_name = None

    def get_inst_state(self, instance):
        return self.state
    get_inst_state.short_description  = "Instance State"

    def get_public_dns_name(self, instance):
        return self.public_dns_name
    get_public_dns_name.short_description  = "Public DNS Name"

    def get_rdp_url(self, instance):
        if self.state == "running":
            return format_html('<a href="/aws_manager/get_rdp/{0}/{1}">RDP File</a>', self.public_dns_name, instance.user_name)
        else:
            return 'Not Available (server not running)'

    get_rdp_url.short_description  = "Remote Desktop File"
    get_rdp_url.allow_tags = True

    def get_connection(self, server):
        """
        Connects to AWS and returns an ec2 connection
        """
        conn = boto3.client('ec2', region_name=server.aws_region, aws_access_key_id=server.aws_access_key, aws_secret_access_key=server.aws_secret_key)
        return conn

    def describe_instance(self, server):
        """
        Connects to AWS and returns an instance description
        """
        conn = self.get_connection(server)
        all_instances = conn.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [server.name]}])
        if not all_instances:
            raise AWSNotFoundException("AWS Instance not found, check settings.")
        inst = all_instances['Reservations'][0]['Instances'][0]
        return inst

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            server = self.get_object(self, object_id)
            inst = self.describe_instance(server)
            self.state = inst['State']['Name']
            self.public_dns_name = inst['PublicDnsName']
            self.readonly_fields = (self.get_inst_state, self.get_public_dns_name, self.get_rdp_url)
        except:
            self.readonly_fields = ()
            messages.add_message(request, messages.ERROR, 'Warning: Server not found.  Please check AWS connection details')

        return super(AWSServerAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

    def action_start_server(self, request, queryset):
        for obj in queryset:
            try:
                obj.start_server()
            except Exception as exc:
                self.message_user(request, "Error: can't start " + obj.name + " server. %s" % exc, level=messages.ERROR)
        self.message_user(request, "%s AWS servers sent start command." % queryset.count())

    action_start_server.short_description = "Start AWS Server"

    def action_stop_server(self, request, queryset):
        for obj in queryset:
            try:
                obj.stop_server()
            except Exception as exc:
                self.message_user(request, "Error: can't stop " + obj.name + " server. %s" % exc, level=messages.ERROR)
        self.message_user(request, "%s AWS servers sent stop command." % queryset.count())

    action_stop_server.short_description = "Stop AWS Server"

    actions = ['action_start_server', 'action_stop_server']






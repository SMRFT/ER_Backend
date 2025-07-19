from rest_framework import serializers
from .models import ERRegister,ERBilling
from bson import ObjectId


# Custom field to handle ObjectId
class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)
    def to_internal_value(self, data):
        return str(data)
    

#ER form
class ERRegisterSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)  # :point_left: Add this line to use custom field
    class Meta:
        model = ERRegister
        fields = '__all__'

#ER Billing
class ERBillingSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)  # :point_left: Add this line to use custom field
    class Meta:
        model = ERBilling
        fields = '__all__'
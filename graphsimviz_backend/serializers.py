import json

from rest_framework import serializers

from graphsimviz_backend.models import ClusterTask

network_types = [('disease_drug', 'disease_drug'),
                 ('disease_variant', 'disease_variant'),
                 ('disease_symptom', 'disease_symptom'),
                 ('disease_gene', 'disease_gene'),
                 ('drug_disease', 'drug_disease'),
                 ('disease_comorbidity', 'disease_comorbidity')]

id_spaces = [('MONDO', 'MONDO'), ('ICD10', 'ICD10')]


class ClusterTaskSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    def get_result(self, obj):
        if obj.result is not None and len(obj.result) > 0:
            return json.loads(obj.result)
        return {}

    class Meta:
        model = ClusterTask
        fields = ['done', 'error', 'result']

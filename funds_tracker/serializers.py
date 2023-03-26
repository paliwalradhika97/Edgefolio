from rest_framework import serializers
from funds_tracker.models import Fund
import io, csv
from django.db import transaction

class FundSerializer(serializers.ModelSerializer):
    inception_date = serializers.DateField(input_formats=['%d/%m/%Y'], required=False, allow_null=True)
    class Meta:
        model = Fund
        fields = "__all__"

class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()

    def save(self, **kwargs):
        decode_csv_file = self.validated_data["file_uploaded"].read().decode("utf-8-sig")

        io_string = csv.reader(io.StringIO(decode_csv_file))
        all_data = [row for row in io_string]

        row_number = 2
        with transaction.atomic():
            for row in all_data[1:]:
                fund_serializer = FundSerializer(data={"name":row[0], "strategy":row[1], "aum":row[2] if row[2] else None, "inception_date":row[3] if row[3] else None})
                if fund_serializer.is_valid():
                    fund_serializer.save()
                else:
                    raise serializers.ValidationError({"file_error":{"row_num":row_number, "errors":fund_serializer.errors}})
                row_number += 1
        
        return self.validated_data


       
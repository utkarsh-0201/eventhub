from rest_framework import serializers
from .models import Event, Reservation


class EventSerializer(serializers.ModelSerializer):
    reservations_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'venue', 'date', 'total_seats',
            'available_seats', 'status', 'created_at', 'reservations_count',
        ]
        read_only_fields = ['created_at']

    def get_reservations_count(self, obj):
        return obj.reservations.filter(status='confirmed').count()

    def validate(self, data):
        total_seats = data.get('total_seats', getattr(self.instance, 'total_seats', None))
        available_seats = data.get('available_seats', getattr(self.instance, 'available_seats', None))

        if total_seats is not None and available_seats is not None:
            if available_seats > total_seats:
                raise serializers.ValidationError(
                    {'available_seats': 'available_seats cannot exceed total_seats.'}
                )
        return data


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = [
            'id', 'event', 'attendee_name', 'attendee_email', 'seats_reserved', 'status', 'created_at',
        ]
        read_only_fields = ['status', 'created_at']

    def validate_seats_reserved(self, value):

        if value < 1:
            raise serializers.ValidationError('Must reserve at least 1 seat.')

        return value

    def validate(self, data):
        event = data.get('event')

        if event.status not in ('upcoming', 'ongoing'):
            raise serializers.ValidationError(
                f'Cannot reserve seats for a {event.status} event.'
            )

        if data.get('seats_reserved', 0) > event.available_seats:

            raise serializers.ValidationError(
                f'Only {event.available_seats} seat(s) available.'
            )
        return data

    def create(self, validated_data):
        from django.db import transaction

        seats_reserved = validated_data['seats_reserved']
        event_id = validated_data['event'].pk

        with transaction.atomic():
            event = Event.objects.select_for_update().get(pk=event_id)
            if seats_reserved > event.available_seats:
                raise serializers.ValidationError(
                    f'Only {event.available_seats} seat(s) available.'
                )
            event.available_seats -= seats_reserved
            event.save()

        validated_data['event'] = event
        return Reservation.objects.create(**validated_data)
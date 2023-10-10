import csv
from django.core.management.base import BaseCommand
from data_logger.models import Hotel, Floor, Room

class Command(BaseCommand):
    help = 'Import data from a CSV file into Hotel, Floor, and Room models'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    hotel_name = row['Hotels'].title().strip()
                    floor_numbers = [int(floor.strip()) for floor in row['Floor'].split(',')]
                    room_numbers = [room.upper().strip() for room in row['Rooms'].split(',')]

                    # Create or get the Hotel
                    hotel, created = Hotel.objects.get_or_create(name=hotel_name)

                    # Create the Floors
                    stat = 1
                    for floor_number in floor_numbers:
                        floor, created = Floor.objects.get_or_create(hotel=hotel, number=floor_number)

                        # Create the Rooms for each floor
                        for room_number in room_numbers:
                            if room_number.startswith(str(stat)):
                                Room.objects.get_or_create(floor=floor, number=room_number)
                        stat += 1

            self.stdout.write(self.style.SUCCESS('CSV data imported successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing CSV data: {str(e)}'))

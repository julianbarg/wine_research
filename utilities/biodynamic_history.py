
class BiodynamicSpider(Spider):
    name = 'biodynamic'


    def _create_csv(self):
        if not os.path.isfile(self.destination):
            with open(self.destination, 'w') as output:
                writer = csv.writer(output)
                writer.writerow(['Name',
                                 'Date',
                                 'Category',
                                 'Address',
                                 'Phone',
                                 'Email',
                                 'Website',
                                 'Short description',
                                 'Description',
                                 'Crops',
                                 'Processed products',
                                 'Cropped_acreage',
                                 'Total_acreage'
                                 ])

    def parse(self):
        yield

    def parse_organizations(self):
        self.process.start()

    def close_parser(self):
        self.process.stop()

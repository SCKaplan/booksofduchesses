# [Books of Ducheses](https://booksofduchesses.com/): Visualizing Women Book Ownership in Late Medieval Francophone Europe: 1350-1500



This project was commissioned by Sarah Watson of Haverford College and S.C Kaplan of Rice University. The projects aims to

* organize, collect, and visualize data about medieval laywomen and their books      
* chart networks of texts, manuscripts, and readers
* challenge narratives of national literary history and assumptions about gendered reading

The primary audience of the site is students or professors researching literary patterns and seeking information (especially in a visually friendly format) about book, book owners, texts, etc. The main tool of the site is the map (based in Leaflet and GeoDjango, usage documented [here](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/MapsOrGeocoding/LeafletMarkerCluster)), which is searchable and displays a popup at each location where a book (green pin) or owner (purple pin) may have existed. Through interaction with the map and the popups, users can navigate to individual owner or book pages, exploring background information and even digital versions of the books themselves. For more information around the purpose, scope and research aims of the project, the original proposal can be found [here](https://docs.google.com/document/d/1UW08KOh60aR89OT8IjKvs6xUFcWAprR3g0JiQmbMsLg/edit).

If you're just beginning with this project, look around the [project plan](https://github.com/HCDigitalScholarship/booksofduchesses/projects/1) to get an idea of the issues that most need attention.

It should be noted that a large portion of the workflow thus far has been very back-end heavy. All our data comes from a haphazardly linked AirTable, so creating the right connections and then moving AirTable/csv formatted data into our more properly linked models is a huge part of this project. Additionaly, we eventually want to hand off control of data entry completely to the professors, so creating mdoels that make sense to non-programmers while also keeping the functionality we need is important. With this goal in mind we center much of the backend on the Book and Owner models, which work with the map through their respective BookLocation and OwnerLocation many to many fields. More information can be found in the in-code documentation.

### Core frameworks
* Python
* Django
* JS/JQuery
* mySQL database and Django admin

### Tools
* [Leaflet](https://leafletjs.com/)
* [GeoDjango](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/)
* [Leaflet Marker Cluster](https://github.com/Leaflet/Leaflet.markercluster) (temporarily at least)
* [Autocomplete Light](https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html) (pending)


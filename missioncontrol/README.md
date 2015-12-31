# Mission Control

Software that is used to manage the Earth to Mars data collection.
To be run on a raspberry pi.

# Wireframes

Look at the [wireframes](wireframes) to see proposed functionality.
What is currently missing is admin view (see below).

# mission control view

* multiple views onto the datasets (photos, temp, humidity etc)
* shows current progress on a projector
* allows pulling of data via API

# upload sample

* allows upload of photo or sample
* accepts updates from teams, uses data to update graphs
* asks science question
* allows pushing data via API

# sample received page

* shows an approved answer to question

# Admin view

* create new data set: date & school name
* export data set
* shutdown 

If above is all that is required can be done at boot if the software detects no new table with correct date. Though that requires date being set correctly.

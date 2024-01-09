document.addEventListener('DOMContentLoaded', function () {
    const locationInput = document.getElementById('location');
    const autocomplete = new google.maps.places.Autocomplete(locationInput);

    autocomplete.addListener('place_changed', function () {
        const selectedPlace = autocomplete.getPlace();
        const location = {
            name: selectedPlace.name,
            address: selectedPlace.formatted_address,
            latitude: selectedPlace.geometry.location.lat(),
            longitude: selectedPlace.geometry.location.lng()
        };

        console.log(location);
    });

    // Fetch doctors based on specialty
    const specialty = 'your_specialty'; // Replace with the actual specialty
    fetchDoctors(specialty);
});

function fetchDoctors(specialty) {
    fetch(`/api/doctors?specialty=${specialty}`)
        .then(response => response.json())
        .then(doctors => {
            // Code to handle the list of doctors
            console.log(doctors);

            // Initialize Google Maps for each doctor
            doctors.forEach(doctor => {
                initMap(doctor.id, doctor.latitude, doctor.longitude);
            });
        })
        .catch(error => {
            console.error('Error fetching doctors:', error);
        });
}

function initMap(doctorId, latitude, longitude) {
    const mapOptions = {
        center: { lat: latitude, lng: longitude },
        zoom: 15,
    };
    const map = new google.maps.Map(document.getElementById('map-container-' + doctorId), mapOptions);

    const marker = new google.maps.Marker({
        position: { lat: latitude, lng: longitude },
        map: map,
        title: 'Doctor Location',
    });
}

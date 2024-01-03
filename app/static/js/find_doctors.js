function fetchDoctors(specialty) {
    fetch(`/api/doctors?specialty=${specialty}`)
        .then(response => response.json())
        .then(doctors => {
            // Code to handle the list of doctors
            console.log(doctors);
        })
        .catch(error => {
            console.error('Error fetching doctors:', error);
        });
}


function populateCities() {
    const citySelect = document.getElementById('city');
    fetch('https://turkiyeapi.cyclic.app/api/v1/provinces?fields=name,areaCode')
        .then(response => response.json())
        .then(data => {
            data.data.forEach(city => {
                const option = document.createElement('option');
                option.value = city.name;
                option.textContent = city.name;
                citySelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching cities:', error));
}

document.addEventListener('DOMContentLoaded', populateCities)

function getTowns() {
    const citySelect = document.getElementById('city');
    const selectedCity = citySelect.value;
    const townSelect = document.getElementById('town');
    townSelect.innerHTML = '<option value="">Select a town</option>';

    if (selectedCity !== '') {
        fetch(`https://turkiyeapi.cyclic.app/api/v1/provinces?name=${selectedCity}`)
            .then(response => response.json())
            .then(data => {
                const districts = data.data[0].districts;
                districts.forEach(district => {
                    const option = document.createElement('option');
                    option.value = district.name;
                    option.textContent = district.name;
                    townSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching towns:', error));
    }
}



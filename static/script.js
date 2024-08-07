// script.js
// Function to select all checkboxes
function SelectAllDays() {
    const checkboxes = document.querySelectorAll('input[name="days"]');
    checkboxes.forEach(checkbox => (checkbox.checked = true));
}


function AddToCallList() {
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const phoneNumber = document.getElementById('phoneNumber').value;
    const groupname = document.getElementById('groupname').value;

    const dataToSave = {
        group_name: groupname,
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber,
    };

    fetch('/add_to_call_list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSave),
    })
        .then(response => response.json())
        .then(result => {
            // Handle the result from the Flask route (e.g., display a success message)
            console.log(result.message);

            // Clear the form fields and selected checkboxes
            document.getElementById('firstName').value = '';
            document.getElementById('lastName').value = '';
            document.getElementById('phoneNumber').value = '';

            document.querySelectorAll('input[name="days"]:checked').forEach(checkbox => (checkbox.checked = false));
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function SaveDays()
{
    // Get selected days of the week
    const selectedDays = Array.from(document.querySelectorAll('input[name="days"]:checked')).map(day => day.value);
    const groupname = document.getElementById('groupname').value;
    
    const dataToSave = {
        group_name: groupname,
        selected_days: selectedDays
    };
    fetch('/save_to_days_of_week', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSave),
    })
        .then(response => response.json())
        .then(result => {

            console.log(result.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function LoadDays()
{
    const groupname = document.getElementById('groupname').value;

    const data = {
        group_name: groupname
    };

    fetch('/load_daysofweek_from_db', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(daysofweek => {
            // Split the daysofweek string into an array of selected days
            const strdaysofweek = JSON.stringify(daysofweek);
            const selectedDays = strdaysofweek.split(', ');
    
            // Get all checkboxes for days of the week
            const checkboxes = document.querySelectorAll('input[name="days"]');
            
            // Check checkboxes if their value is in the selectedDays array
            checkboxes.forEach(checkbox => {
                if (strdaysofweek.includes(checkbox.value)) {
                    checkbox.checked = true;
                } else {
                    checkbox.checked = false;
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function DisplayCallList()
{
    // Handle the generated schedule
    const callersTable = document.getElementById('callersTable').getElementsByTagName('tbody')[0];
    callersTable.innerHTML = ''; // Clear existing content

    const groupname = document.getElementById('groupname').value;
    const data = {
        group_name: groupname
    };

    fetch('/load_callers_from_db', {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {

            if (data && data.callers) {
                console.log(data.callers)
                data.callers.forEach((caller)=>{
                    const row = callersTable.insertRow();
                    const cellGroupName = row.insertCell(0);
                    const cellFirstName = row.insertCell(1);
                    const cellLastName = row.insertCell(2);
                    const cellPhoneNumber = row.insertCell(3);
                    cellGroupName.textContent = caller.group_name;
                    cellFirstName.textContent = caller.first_name;
                    cellLastName.textContent = caller.last_name;
                    cellPhoneNumber.textContent = caller.phone_number;
                 });
                }
            }
        )
        .catch(error => {
            console.error('Error:', error);
        });
}





// TODO
function generateCallSchedule() {
    const submittedDataList = document.getElementById('submittedDataList');
    const dataItems = submittedDataList.getElementsByTagName('li');
    const data = [];

    for (let i = 0; i < dataItems.length; i++) {
        data.push(dataItems[i].textContent);
    }

    fetch('/generate_call_schedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(schedule => {
            // Handle the generated schedule
            console.log('Generated Schedule:', schedule);

            const generatedCallScheduleList = document.getElementById('generatedCallSchedule');
            generatedCallScheduleList.innerHTML = ''; // Clear existing content

            if (schedule.schedule) {
                // If the JSON response has a 'schedule' property, use it
                const listItem = document.createElement('li');
                listItem.textContent = schedule.schedule;
                generatedCallScheduleList.appendChild(listItem);
            } else {
                // If there's no 'schedule' property, just add the entire response
                const listItem = document.createElement('li');
                listItem.textContent = JSON.stringify(schedule);
                generatedCallScheduleList.appendChild(listItem);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


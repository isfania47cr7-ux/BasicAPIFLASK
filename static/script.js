const API_URL="http://127.0.0.1:5000/students";

const form = document.getElementById("student-form");


const studentId =
    document.getElementById("student-id");

const nameInput =
    document.getElementById("name");

const courseInput =
    document.getElementById("course");

const ageInput =
    document.getElementById("age");

const tableBody =
    document.getElementById("student-table-body");

const formTitle =
    document.getElementById("form-title");

const submitButton =
    document.getElementById("submit-button");

const cancelButton =
    document.getElementById("cancel-button");

document.addEventListener("DOMContentLoaded",function(){
    loadStudents();

});

async function loadStudents(){
    try{
        const response = await fetch(API_URL);
        const students=await response.json();
        displayStudents(students.data)
    }
    catch(error){
        console.error("Error loading students:",error);
    }
}

function displayStudents(students) {

    tableBody.innerHTML = "";

    students.forEach(function (student) {

        const row = document.createElement("tr");

        row.innerHTML = `

            <td>${student.id}</td>

            <td>${student.name}</td>

            <td>${student.course}</td>

            <td>${student.age}</td>

            <td>

                <button
                    class="edit-button"
                    onclick="editStudent(${student.id})">
                    Edit
                </button>

                <button
                    class="delete-button"
                    onclick="deleteStudent(${student.id})">
                    Delete
                </button>

            </td>

        `;

        tableBody.appendChild(row);

    });
}
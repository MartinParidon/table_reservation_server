console.log('Script loaded');

// function reserveSeat(seat) {
//   const seatNumber = seat.dataset.seat;
//   const status = seat.parentElement.previousElementSibling.querySelector(".status");
//
//   // Check if the seat is already reserved
//   if (status.classList.contains("red")) {
//     alert("This seat is already reserved.");
//     return;
//   }
//
//   // Prompt the user to enter their name
//   const name = prompt("Please enter your name:");
//
//   // Send an AJAX POST request to the server to reserve the seat
//   $.ajax({
//     url: "/reserve",
//     type: "POST",
//     data: JSON.stringify({ seat: seatNumber, name: name }),
//     contentType: "application/json; charset=utf-8",
//     dataType: "json",
//     success: function (result) {
//       if (result.success) {
//         // Update the status of the seat to "reserved"
//         status.classList.remove("green");
//         status.classList.add("red");
//
//         // Add the name of the person who reserved the seat
//         const nameCell = seat.parentElement.nextElementSibling;
//         nameCell.textContent = name;
//       } else {
//         alert(result.message);
//       }
//     },
//     error: function (xhr, status, error) {
//       alert("Error: " + error);
//     },
//   });
// }

$(document).ready(function() {
  $('.reserve-btn').click(function() {
    // Get the seat number and status
    var seat_number = $(this).data('seat');
    var status = $(this).closest('tr').find('.status').attr('class').split(' ')[1];

    // Check if the seat is already reserved
    if (status == 'red') {
      alert('This seat is already reserved. Please choose another seat.');
      return;
    }

    // Prompt the user to enter their name
    var name = prompt('Please enter your name:');
    if (!name) {
      alert('You must enter a name to reserve a seat.');
      return;
    }

    // Send a POST request to reserve the seat
    $.post('/reserve', {
      seat: seat_number,
      name: name
    }, function(data) {
      // Update the table with the new seat status
      var new_status = data.status == 'success' ? 'red' : 'green';
      $('.reserve-btn[data-seat=' + seat_number + ']').closest('tr').find('.status').removeClass('green red').addClass(new_status);
      // Update the table with the name of the person who reserved the seat
      $('.reserve-btn[data-seat=' + seat_number + ']').closest('tr').find('.name').text(name);
    });
  });
});

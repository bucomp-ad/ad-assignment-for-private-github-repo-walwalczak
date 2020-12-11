//POST new board
function submit(boardname){
  $.ajax({
    type: 'POST',
    url: `/trello/${boardname}`,
    dataType: "json",
    success: function(data){
      console.log('Success', data)
      $('#response').html(`Your board <i>${data.name}</i> 
            has been created: <a href="${data.url}" target="_blank">Click here to view</a>`)
  },
  error:function(errMsg){
    $('#response').html(errMsg);
  }
});
}

$("#submit").click(function(){
  let name = document.getElementById("board-name-input").value
  submit(name)
});
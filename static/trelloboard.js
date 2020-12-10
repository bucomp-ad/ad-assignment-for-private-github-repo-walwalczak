

function submit(boardname){
  console.log("Name in func " + boardname)
  $.ajax({
    type: 'POST',
    url: `/trello/${boardname}`,
    dataType: "json",
    success: function(data){
      console.log('Success', data)
      $('#response').html(data)
  },
  error:function(){
    console.log('in error');
  }
});
}


$("#submit").click(function(){
  let name = document.getElementById("board-name-input").value
  submit(name)
});

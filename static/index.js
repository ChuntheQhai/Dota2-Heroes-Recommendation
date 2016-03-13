
var ourTeams = {'team':[]};
var theirTeams = {'team':[]};


if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    alert("Please use desktop browser! :)");
    window.location.href = "https://www.google.com"; 
}


if(!Array.prototype.contains) {
  Array.prototype.contains = function(k) {
    for(var i=0; i < this.length; i++){
      if(this[i] === k){
        return true;
      }
    }
    return false;
  }
}

function removeElementsWithValue(arr, val) {
    var i = arr.length;
    while (i--) {
        if (arr[i] === val) {
            arr.remove(i);
        }
    }
    return arr;
}

Array.prototype.remove = function(index) {
    this.splice(index, 1);
}

// function onPageLoad(){
// 	new Ajax.Request('static/data/heroes.json', {
// 		method: 'get',
// 		onSuccess: function(transport){
			
// 		}
// 	});
// }

function targetSlotToTeamId(slot){
    var result = 0;
    switch(slot) {
        case "1000":
            result = 0;
            break;
        case "2000":
            result = 1;
            break;
        case "3000":
            result = 2;
            break;
        case "4000":
            result = 3;
            break;
        case "5000":
            result = 4;
            break;
        case "6000":
            result = 5;
            break;
        case "7000":
            result = 6;
            break;
        case "8000":
            result = 7;
            break;
        case "9000":
            result = 8;
            break;
        case "10000":
            result = 9;
            break;
        default:
            break;
    }
    return result;
}

jQuery(document).on("click", ".dotaPickerModal", function(){
        jQuery('#myModal').modal('show');
        var slotId = jQuery(this).data('id');
        jQuery('#targetslot').val(slotId);
});


jQuery(document).ready(function($){
    jQuery(".hero-selected").on("click",function(){
        heroId = $(this).attr('id');

        if(ourTeams.team.contains(heroId) || theirTeams.team.contains(heroId)){
            alert("Hero is selected. Please choose another.");
        }else{
            src = "/static/images/hero_"+heroId+".png";
            var targetSlot = document.getElementById('targetslot').value;

            $(targetSlot).attr('src',src);
            var targetSlotId = "#" + targetSlot + " img";

            //var captionId = "#" + targetSlot + " .caption";

            $(targetSlotId).attr('src',src);
            jQuery(targetSlotId).css('display','block');



            var slotPosition = targetSlotToTeamId(targetSlot);

            if(slotPosition >= 5){
                theirTeams.team[slotPosition-5] = heroId;
            }else{
                ourTeams.team[slotPosition] = heroId;
            }

            requestSuggestions();
            $('#myModal').modal('hide');
        }
    });

    //jQuery(".select_recommend_hero").on("click", function(){
    jQuery(document).on("click",".select_recommend_hero", function(){
        heroId = $(this).attr('id');
        if(ourTeams.team.contains(heroId) || theirTeams.team.contains(heroId)){
            alert("Hero is selected. Please choose another.");
        }else{
            src = "/static/images/hero_"+heroId+".png";

            var done =false;
            var targetSlot;

            if(ourTeams.team.length < 5){
                var i = ourTeams.team.length;
                targetSlot = String(i+1)+"000";
                done = true;    
            }

            if(!done){
                // Replace the last slot if all slots used.
                targetSlot = "5000";
            }


            var targetSlotId = "#" + targetSlot + " img"
            $(targetSlotId).attr('src',src);

            jQuery(targetSlotId).css('display','block');


            var slotPosition = targetSlotToTeamId(targetSlot);


            ourTeams.team[slotPosition] = heroId;
            requestSuggestions();
        }
    });
});


function insertRecommendHero(id,name){
    var filas = document.getElementById("recommendation_table").rows.length;
    var x = document.getElementById("recommendation_table").insertRow(filas);
    var y = x.insertCell(0);
    y.innerHTML = "<a href='javascript:;' class='select_recommend_hero' id="+id+"><img src='static/images/hero_"+id+".png'/><span>"+name+"</span></a>";   
}


function process(resp){
    jQuery('#success_rate').css('display','block');
    document.getElementById("winning-chance").innerHTML = (100*resp.prob_x).toFixed(0)+"%";

    if(resp.x.length == 0){
        document.getElementById("recommend_container").style.display = "none";
    }else{
        document.getElementById("recommend_container").style.display = "block";
        var table = document.getElementById("recommendation_table");
        while(table.rows.length > 0) {
          table.deleteRow(0);
        }
        for(var i = 0; i < resp.x.length;i++){
            insertRecommendHero(resp.x[i].id, resp.x[i].localized_name);
        }
    }
}

function requestSuggestions(){
    var x,y;
    x = removeElementsWithValue(ourTeams.team,0);
    y = removeElementsWithValue(theirTeams.team,0);
  
    var new_x = String(x).replace(/,+/g,',');
    var new_y = String(y).replace(/,+/g,',');


    new Ajax.Request('api/recommend/?'+'x='+new_x+'&y='+new_y, {
        method: 'get',
        onSuccess: function(response) {
            process(response.responseText.evalJSON(true));
        }
    });
}





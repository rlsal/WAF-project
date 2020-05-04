jQuery(document).ready(function($) {
    $.ajax({url: "http://localhost:5000/config",dataType:'json', success: function(result){
        // console.log(result['attack_types'].length);
        var systemMode = result['system_mode'];
        var prohibitedFileTypes = result['prohibited_file_types'];
        $('#system_mode').val(systemMode);
        $('#prohibited_file_types').val(prohibitedFileTypes);
        for (var i = 0; i < result['attack_types'].length; i++) {
           console.log(result['attack_types'][i]);
           $('div[data-attack-type=' + result["attack_types"][i].name +']').find('.attack-action').val(result['attack_types'][i].per_attack_action); 
           $('div[data-attack-type=' + result["attack_types"][i].name +']').find('.attack-report').val(result['attack_types'][i].report_type);
        };
    }});
    var jsonObj = {};
    $( ".btn-default" ).click(function(e) {
        e.preventDefault();
        console.log($("#prohibited_file_types").val());
        var systemMode = $("#system_mode").val();
        var prohibitedFileTypes = $("#prohibited_file_types").val();

        jsonObj['system_mode'] = systemMode;
        jsonObj['prohibited_file_types'] = prohibitedFileTypes;

        jsonObj['attack_types'] = [];


        $.each($('div[data-attack-type]'), function(key, value){
            var obj = {
                'name': $(value).attr('data-attack-type'),
                'per_attack_action': $(value).find($('.attack-action')).val(),
                'report_type': $(value).find($('.attack-report')).val()
            };
            jsonObj['attack_types'].push(obj);
        });

        // console.log(JSON.stringify(jsonObj));
        $.post({url: "http://localhost:5000/config",dataType:'json', contentType: "application/json; charset=utf-8",data: JSON.stringify(jsonObj),  success: function(result){
            console.log(result);
        }});
    });
});    
   
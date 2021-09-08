'use strict';

function setCssDegForGauge() {
    var tanksGauges = document.querySelectorAll('.tanks__gauge');
    for (var i = 0; i < tanksGauges.length; i++) {
        var percent = tanksGauges[i].getAttribute('data-percent');
        if (percent <= 0) {
            continue;
        } else if (percent > 100) {
            percent = 100;
        }

        var donut = tanksGauges[i].querySelector(
            '.tanks__donut-rotate__wrapper');
        var degDonut = Math.round((percent * 1.8) + 180) + 'deg';
        setCss(donut, degDonut);

        var arrow = tanksGauges[i].querySelector('.tanks__rotate-arrow');
        var degArrow = Math.round(percent * 1.8) + 'deg';
        setCss(arrow, degArrow);

    }

    function setCss(elem, deg) {
        elem.style.WebkitTransform = 'rotate(' + deg + ')';
        elem.style.MsTransform = 'rotate(' + deg + ')';
        elem.style.transform = 'rotate(' + deg + ')';
    }
}


function update_messages(messages){
    $("#div_messages").html("");
    $.each(messages, function (i, m) {
        $("#div_messages").append("<div class='alert alert-"+m.tags+"''>"+m.message+"</div>");
    });
}

function confirm(company_id, heading, question, callback, callbackArgs) {

    var confirmModal = $('#confirm-modal');

    $('#confirm-modal .modal-title').text(heading);
    $('#confirm-modal .question').html(question);

    confirmModal.find('#okButton').click(function(event) {
        if (callbackArgs){
            callback(company_id, callbackArgs);
        }else{
            callback(company_id);
        }
        confirmModal.modal('hide');
    });

    confirmModal.find('#closeButton').click(function(event) {
        confirmModal.modal('hide');
    });
    confirmModal.modal('show');
}



function parseDjangoData(data){
    data = data.replace(/&(l|g|quo)t;/g, function(a,b){
            return {
                l   : '<',
                g   : '>',
                quo : '"'
            }[b];
        });
    data = data.replace(/u'/g, '\'')
    data = data.replace(/'/g, '\"')

    return JSON.parse(data);

}

function clearDeleteModalData(){
    $('#confirm-id').text('');
    $('#confirm-username').text('')
}

$('#confirmDeleteModal').on('hidden.bs.modal', function () {
  clearDeleteModalData();
});

function deleteUser(company_id){
    var user_id = $('#confirm-id').text();

    $.ajax({
        async: false,
        type: "POST",
        processData: false,
        contentType: false,
        url: "/a/"+company_id+"/delete/user/"+user_id,

        success: function(response) {
            var result = JSON.parse(response);
            update_messages(result.messages);
            if (result.error) {
                console.log(result);
            } else {
                $('#row_id_'+user_id).parent().parent().fadeOut(500);
            }
        }
    });
}

function confirmDeleteUser(user_id){
    var username = $('#row_id_'+user_id).parent().parent().find('.username').text();
    $('#confirm-id').text(user_id);
    $('#confirm-username').text(username);
    $('#confirmDeleteModal').modal();

}


function updateTankInfo(tank_id){
    var low_volume = $('#edit-tank-modal .low_volume').val()
    var low_volume_email = $('#edit-tank-modal .low_volume_email').val()
    var reorder_volume = $('#edit-tank-modal .reorder_volume').val()
    var reorder_volume_email = $('#edit-tank-modal .reorder_volume_email').val()
    var max_temperature = $('#edit-tank-modal .max_temperature').val()
    var max_temperature_email = $('#edit-tank-modal .max_temperature_email').val()
    var max_water = $('#edit-tank-modal .max_water_volume').val()
    var max_water_email = $('#edit-tank-modal .max_water_volume_email').val()

    $('#tank-'+tank_id+' .low-volume').text(low_volume);
    $('#tank-'+tank_id+' .low-volume-email').text(low_volume_email);
    $('#tank-'+tank_id+' .reorder-volume').text(reorder_volume);
    $('#tank-'+tank_id+' .reorder-volume-email').text(reorder_volume_email);
    $('#tank-'+tank_id+' .max-temperature').text(max_temperature);
    $('#tank-'+tank_id+' .max-temperature-email').text(max_temperature_email);
    $('#tank-'+tank_id+' .max-water').text(max_water);
    $('#tank-'+tank_id+' .max-water-email').text(max_water_email);
}

function editTankData(company_id, tank_id){
  var data = new FormData($('#edit-tank-modal form').get(0));

  $.ajax({
    async: false,
    type: "POST",
    processData: false,
    contentType: false,
    url: "/content/a/"+company_id+"/tank/"+tank_id+"/edit/alerts/",
    data: data,

    success: function(response) {
        var result = JSON.parse(response);
        if (result.error) {
            console.log(result.error_text);
        } else {
          $('#edit-tank-modal').modal('hide');
          updateTankInfo(tank_id);
        }
    }
  });

  $('#btn-save').prop("disabled", false);
};


function clearTankModal(){
    $('#edit-tank-modal .low_volume').val('');
    $('#edit-tank-modal .low_volume_email').val('');
    $('#edit-tank-modal .reorder_volume').val('');
    $('#edit-tank-modal .reorder_volume_email').val('');
    $('#edit-tank-modal .max_temperature').val('');
    $('#edit-tank-modal .max_temperature_email').val('');
    $('#edit-tank-modal .max_water_volume').val('');
    $('#edit-tank-modal .max_water_volume_email').val('');
}

function prepareTankModal(tank_id){
    var low_volume = $('#tank-'+tank_id+' .low-volume').text();
    var low_volume_email = $('#tank-'+tank_id+' .low-volume-email').text();
    var reorder_volume = $('#tank-'+tank_id+' .reorder-volume').text();
    var reorder_volume_email = $('#tank-'+tank_id+' .reorder-volume-email').text();
    var max_temperature = $('#tank-'+tank_id+' .max-temperature').text();
    var max_temperature_email = $('#tank-'+tank_id+' .max-temperature-email').text();
    var max_water = $('#tank-'+tank_id+' .max-water').text();
    var max_water_email = $('#tank-'+tank_id+' .max-water-email').text();
    var tank_name = $('#tank-'+tank_id+' .tank-name').text();

    $('#edit-tank-modal .low_volume').val(low_volume);
    $('#edit-tank-modal .low_volume_email').val(low_volume_email);
    $('#edit-tank-modal .reorder_volume').val(reorder_volume);
    $('#edit-tank-modal .reorder_volume_email').val(reorder_volume_email);
    $('#edit-tank-modal .max_temperature').val(max_temperature);
    $('#edit-tank-modal .max_temperature_email').val(max_temperature_email);
    $('#edit-tank-modal .max_water_volume').val(max_water);
    $('#edit-tank-modal .max_water_volume_email').val(max_water_email);
    $('#edit-tank-modal .tank-name').text(tank_name);
}

function showTankModal(company_id, tank_id){
    prepareTankModal(tank_id);
    $("#btn-edit").click(function(){ editTankData(company_id, tank_id); });
    $("#edit-tank-modal").modal('show');
}

$('#edit-tank-modal').on('hidden.bs.modal', function () {
    clearTankModal();
});

var old_html = $('.summary').html()

function cancelEditSummary(){
    $('.summary').html(old_html);
}


function updateTankSummary(data){
    // Change inputs for divs
    $('.summary .title').replaceWith('<div class="summary__field title">'+data.title+'</div>');
    $('.summary .number').replaceWith('<div class="summary__field number">'+data.number+'</div>');
    $('.summary .address').replaceWith('<div class="summary__field address">'+data.address+'</div>');
    $('.summary .phone').replaceWith('<div class="summary__field phone">'+data.phone+'</div>');
    $('.summary .contact').replaceWith('<div class="summary__field contact">'+data.contact+'</div>');
    $('.summary .supplier').replaceWith('<div class="summary__field supplier">'+data.fuel_supplier+'</div>');


    // Disable some fields that cannot be edited
    $('.summary .gps').attr('style', '');
    $('.summary .status').attr('style', '');


    // Show edit icon
    $('.summary .summary__title i').show();

    // Remove btns div
    $('.summary .btn-summary-container').remove()
}

function saveSummary(company_id, site_id){

    var title = $('.summary .title').val();
    var number = $('.summary .number').val();
    var address = $('.summary .address').val();
    var phone = $('.summary .phone').val();
    var contact = $('.summary .contact').val();
    var fuel_supplier = $('.summary .supplier').val();

    var data = {
        "title": title,
        "number": number,
        "address": address,
        "phone": phone,
        "contact": contact,
        "fuel_supplier": fuel_supplier
    }

    $.ajax({
        async: false,
        type: "POST",
        url: "/content/a/"+company_id+"/site/"+site_id+"/edit/summary/",
        data: data,

        success: function(response) {
            var result = JSON.parse(response);
            update_messages(result.messages);
            if (result.error) {
                console.log(result.error_text);
            } else {
                updateTankSummary(data);
            }
        }
  });
}

function editSiteSummary(company_id, site_id){
    var title = $('.summary .title').text();
    var number = $('.summary .number').text();
    var address = $('.summary .address').text();
    var phone = $('.summary .phone').text();
    var contact = $('.summary .contact').text();
    var fuel_supplier = $('.summary .supplier').text();
    var disabled_css = "background: gray;color: gainsboro;cursor: not-allowed;";
    var save_btn = '<button type="button" class="btn btn-success" onClick="saveSummary('+company_id+', '+site_id+')">Modify</button>';
    var cancel_btn = '<button type="button" class="btn btn-danger" onClick="cancelEditSummary()">Cancel</button>';
    var extra_space = "&nbsp;&nbsp;&nbsp;"

    // Change divs for inputs
    $('.summary .title').replaceWith('<input type="text" class="form-control title" name="title" value="'+title+'"/>');
    $('.summary .number').replaceWith('<input type="text" class="form-control number" name="number" value="'+number+'"/>');
    $('.summary .address').replaceWith('<input type="text" class="form-control address" name="address" value="'+address+'"/>');
    $('.summary .phone').replaceWith('<input type="text" class="form-control phone" name="phone" value="'+phone+'"/>');
    $('.summary .contact').replaceWith('<input type="text" class="form-control contact" name="contact" value="'+contact+'"/>');
    $('.summary .supplier').replaceWith('<input type="text" class="form-control supplier" name="fuel_supplier" value="'+fuel_supplier+'"/>');

    // Disable some fields that cannot be edited
    $('.summary .gps').attr('style', disabled_css);
    $('.summary .status').attr('style', disabled_css);

    // Hide edit icon
    $('.summary .summary__title i').hide();

    // Append buttons to summary
    $('.summary').append('<div class="text-center btn-summary-container">'+save_btn+extra_space+cancel_btn+'</div>');
}


function confirmDelivery(company_id, delivery_id){

  $.ajax({
    async: false,
    type: "POST",
    url: "/content/a/"+company_id+"/delivery/"+delivery_id+"/confirm/",

    success: function(response) {
        var result = JSON.parse(response);
        update_messages(result.messages);
        if (result.error) {
            console.log(result.error_text);
        } else {
            var current_row = $('.tr-'+delivery_id);
            var last_unconfirmed = $('tr.unconfirmed:last');
            current_row.attr('style', '');
            current_row.insertAfter(last_unconfirmed)
            current_row.find('.confirm-action button.btn-success').remove();
            current_row.removeClass('unconfirmed')
            current_row.find('.confirmed').html('<i class="glyphicon glyphicon-ok"></i>');

        }
    }
  });

};

function updateDeliveryVolume(company_id, delivery_id, old_value){
    var dv = $('#delivery-volume-'+delivery_id).val()
    var data = {
        'delivery_volume': dv
    };
    $.ajax({
        async: true,
        type: "POST",
        url: "/content/a/"+company_id+"/delivery/"+delivery_id+"/update/volume/",
        data: data,

        success: function(response) {
            var result = JSON.parse(response);
            update_messages(result.messages);
            if (result.error) {
                console.log(result.error_text);
            } else {
                // Get onclick string for confirm action button
                var onclick_val = $('.tr-'+delivery_id+' .confirm-action button').attr("onclick");

                // Update the onclick text used for delivery_volume with current delivery volume
                onclick_val = onclick_val.replace(old_value, dv);

                // Update the button onclick value with new string
                $('.tr-'+delivery_id+' .confirm-action button').attr("onclick", onclick_val);

                // Remove the input for the delivery volume with the current delivery volume
                $('.tr-'+delivery_id+' .delivery_volume').html(parseFloat(dv).toFixed(2));
            }
        }
    });
}

function editDeliveryVolume(company_id, delivery_id){
    var current_volume = $('.tr-'+delivery_id+' .delivery_volume').text();
    var old_value = $('.tr-'+delivery_id+' .delivery_volume').text();
    // If input is already shown, nothing happens
    if ($('#delivery-volume-'+delivery_id).length )
        return;

    var new_element = '\
        <div class="input-group"> \
            <input \
                style="color:black;" \
                class="form-control" \
                type="number" \
                name="delivery-volume" \
                onkeydown="javascript: if(event.keyCode == 13) updateDeliveryVolume('+company_id+', '+delivery_id+', '+old_value+');" \
                id="delivery-volume-'+delivery_id+'" \
                value="'+current_volume+'" \
            /> \
            <span class="input-group-btn"> \
                <button class="btn btn-default" type="button" onclick="updateDeliveryVolume('+company_id+', '+delivery_id+', '+old_value+');"> \
                    <i class="glyphicon glyphicon-floppy-save"></i> \
                </button> \
            </span> \
    </div>';


    $('.tr-'+delivery_id+' .delivery_volume').html(new_element);
}



function updateTransactionVolume(company_id, transaction_id){
    var volume = $('#transaction-volume-'+transaction_id).val();
    var comments = $('#transaction-comments-'+transaction_id).val();
    var button_title = "Edit";
    var data = {
        'volume': volume,
        'comments': comments
    };
    $.ajax({
        async: true,
        type: "POST",
        url: "/content/a/"+company_id+"/transaction/"+transaction_id+"/update/volume/",
        data: data,

        success: function(response) {
            var result = JSON.parse(response);
            var new_button = '\
                <button class="btn btn-default" type="button" title='+button_title+' data-toggle="tooltip" onclick="editTransactionVolume('+company_id+', '+transaction_id+');"> \
                    <i class="glyphicon glyphicon-pencil"></i> \
                </button>';
            update_messages(result.messages);
            if (result.error) {
                console.log(result.error_text);
            } else {
                // Remove the input for the delivery volume with the current delivery volume
                $('.tr-'+transaction_id+' .volume').html(parseFloat(volume).toFixed(2));
                $('.tr-'+transaction_id+' .comments').html(comments);
                $('.tr-'+transaction_id+' .confirm-action').html(new_button);
            }
        }
    });
}

function editTransactionVolume(company_id, transaction_id){
    var current_volume = $('.tr-'+transaction_id+' .volume').text();
    var current_comments = $('.tr-'+transaction_id+' .comments').text();

    // If input is already shown, nothing happens
    if ($('#transaction-volume-'+transaction_id).length )
        return;

    var new_volume_element = '\
        <div class="input-group"> \
            <input \
                style="color:black;" \
                class="form-control" \
                type="number" \
                name="volume" \
                onkeydown="javascript: if(event.keyCode == 13) updateTransactionVolume('+company_id+', '+transaction_id+');" \
                id="transaction-volume-'+transaction_id+'" \
                value="'+current_volume+'" \
            /> \
    </div>';

    var new_comments_element = '\
        <div class="input-group"> \
            <input \
                style="color:black;" \
                class="form-control" \
                type="text" \
                name="comments" \
                onkeydown="javascript: if(event.keyCode == 13) updateTransactionVolume('+company_id+', '+transaction_id+');" \
                id="transaction-comments-'+transaction_id+'" \
                value="'+current_comments+'" \
            /> \
        </div>';

    var new_button = '\
        <button class="btn btn-default" type="button" onclick="updateTransactionVolume('+company_id+', '+transaction_id+');"> \
            <i class="glyphicon glyphicon-floppy-save"></i> \
        </button>';
    $('.tr-'+transaction_id+' .volume').html(new_volume_element);
    $('.tr-'+transaction_id+' .comments').html(new_comments_element);
    $('.tr-'+transaction_id+' .confirm-action').html(new_button);
}


function getVolumeProcessedForCompany(company_id, start_date, end_date){
    var user_id = $('#confirm-id').text();
    var volumeUrl = "/content/a/"+company_id+"/volume/processed/";

    if (start_date && end_date){
        volumeUrl+="?start_date="+start_date+"&end_date="+end_date;
    }else if (start_date){
        volumeUrl+="?start_date="+start_date
    }else if (end_date){
        volumeUrl+="?end_date"+end_date;
    }

    return $.ajax({
        async: true,
        type: "GET",
        url: volumeUrl,

        success: function(response) {
            var result = JSON.parse(response);
            return result;
        }
    });
}

function getVolumeProcessedForSite(company_id, site_id, start_date, end_date){
    var user_id = $('#confirm-id').text();
    var volumeUrl = "/content/a/"+company_id+"/volume/processed/"+site_id+"/";

    if (start_date && end_date){
        volumeUrl+="?start_date="+start_date+"&end_date="+end_date;
    } else if (start_date){
        volumeUrl+="?start_date="+start_date
    } else if (end_date){
        volumeUrl+="?end_date"+end_date;
    }

    return $.ajax({
        async: true,
        type: "GET",
        url: volumeUrl,

        success: function(response) {
            var result = JSON.parse(response);
            return result;
        }
    });
}

function getConnections(company_id, start_date, end_date){
    var user_id = $('#confirm-id').text();
    var volumeUrl = "/content/a/"+company_id+"/connections/"

    if (start_date && end_date){
        volumeUrl+="?start_date="+start_date+"&end_date="+end_date;
    }else if (start_date){
        volumeUrl+="?start_date="+start_date
    }else if (end_date){
        volumeUrl+="?end_date="+end_date;
    }

    return $.ajax({
        async: true,
        type: "GET",
        url: volumeUrl,

        success: function(response) {
            var result = JSON.parse(response);
            return result;
        }
    });
}
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});
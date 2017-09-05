$( document ).ready(function() {
    $("#loadButton").on("click", function(){
        var selectionValue = $('#selectData').val();
    	$.ajax({
    	    type: "POST",
    	    url: '/handle_data',
            data: {selectData: selectionValue},
    	    success: function(data){
    	        $('#firstPlotDiv').html(data.firstPlotDiv);
    	        $('#firstPlotScript').html(data.firstPlotScript);
    	        $('#origPlotDiv').html(data.origPlotDiv);
        		$('#origPlotScript').html(data.origPlotScript);
    	        $('#ampPlotDiv').html(data.ampPlotDiv);
        		$('#ampPlotScript').html(data.ampPlotScript);
    	        $('#freqPlotDiv').html(data.freqPlotDiv);
        		$('#freqPlotScript').html(data.freqPlotScript);
                $('#graphBlock').css('display','initial');
                $('#paramsBlock').css('display','initial');

                if (selectionValue == 'Stock') {
                    $('#origDataText').html('Apple Inc stock');
                }
                else if (selectionValue == 'Weather') {
                    $('#origDataText').html('Weather data');
                }
                else if (selectionValue == 'Random') {
                    $('#origDataText').html('Random data');
                }
                },
    	    error: function(error){
        		console.log(error);
    	    }
        })
    });
    $('#fourierN').on("change", function(){
        var n = $('#fourierN').val();
        var selectionValue = $('#selectData').val();
        $.ajax({
            type: "POST",
            url: '/update_fourier',
            data: {fourierN: n, selectData: selectionValue},
            success: function(data) {
                $('#origPlotDiv').html(data.origPlotDiv);
        		$('#origPlotScript').html(data.origPlotScript);
                $('#ampPlotDiv').html(data.ampPlotDiv);
                $('#ampPlotScript').html(data.ampPlotScript);
                $('#freqPlotDiv').html(data.freqPlotDiv);
                $('#freqPlotScript').html(data.freqPlotScript);
                $('#aproxValue').html(n)
            },
            error: function(error){
                console.log(error);
            }
        })
    });

});

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
        })
});

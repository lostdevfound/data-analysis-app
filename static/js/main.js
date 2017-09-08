$( document ).ready(function() {
    $("#computeButton").on("click", function(){
        var selectionValue = $('#selectData').val();
    	$.ajax({
    	    type: "POST",
    	    url: '/compute',
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
    	        $('#trandPlotDiv').html(data.trandPlotDiv);
        		$('#trandPlotScript').html(data.trandPlotScript);
                $('#trandPlotDiv').html(data.trandPlotDiv);
                $('#trandPlotScript').html(data.trandPlotScript);
                $('#graphBlock').css('display','initial');
                $('#paramsBlock').css('display','initial');
                $('#aproxValue').html(1)
                $('#fourierN').val(1)

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
                $('#trandPlotDiv').html(data.trandPlotDiv);
                $('#trandPlotScript').html(data.trandPlotScript);
                $('#aproxValue').html(n)
            },
            error: function(error){
                console.log(error);
            }
        })
    });

});

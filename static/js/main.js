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
    	        $('#trendPlotDiv').html(data.trendPlotDiv);
        		$('#trendPlotScript').html(data.trendPlotScript);
                $('#trendPlotDiv').html(data.trendPlotDiv);
                $('#trendPlotScript').html(data.trendPlotScript);
                $('#graphBlock').css('display','initial');
                $('#paramsBlock').css('display','initial');
                $('#aproxValue').html(2)
                $('#fourierN').val(2)

                if (selectionValue == 'Stock') {
                    $('#origDataText').html('Apple Inc stock');
                }
                else if (selectionValue == 'Weather') {
                    $('#origDataText').html('British Columbia. Mean temperature per month');
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
            beforeSend: function(){
                $('.loader').show()
            },
            success: function(data) {
                $('#origPlotDiv').html(data.origPlotDiv);
        		$('#origPlotScript').html(data.origPlotScript);
                $('#ampPlotDiv').html(data.ampPlotDiv);
                $('#ampPlotScript').html(data.ampPlotScript);
                $('#freqPlotDiv').html(data.freqPlotDiv);
                $('#freqPlotScript').html(data.freqPlotScript);
                $('#trendPlotDiv').html(data.trendPlotDiv);
                $('#trendPlotScript').html(data.trendPlotScript);
                $('#aproxValue').html(n);
                $('.loader').hide()
            },
            error: function(error){
                console.log(error);
            }
        })
    });

    $('#convolutionSlider').on('change', function() {
        var selectionValue = $('#selectData').val();
        var convFactor = $('#convolutionSlider').val()
        var n = $('#fourierN').val();

        $.ajax({
            type: "POST",
            url: '/update_trend',
            data: {convolutionFactor: convFactor, selectData: selectionValue, fourierN: n, type: 'highFreq'},
            beforeSend: function(){
                $('.loader').show()
            },
            success: function(data) {
                $('#trendPlotDiv').html(data.trendPlotDiv);
                $('#trendPlotScript').html(data.trendPlotScript);
                $('#convolutionValue').html(convFactor);
                $('#detrendSlider').val(0);
                $('#detrendValue').html(0);
                $('.loader').hide()
            },
            error: function(error){
                console.log(error);
            }
        })
    });

    $('#detrendSlider').on('change', function() {
        var selectionValue = $('#selectData').val();
        var convFactor = $('#detrendSlider').val()
        var n = $('#fourierN').val();

        $.ajax({
            type: "POST",
            url: '/update_trend',
            data: {convolutionFactor: convFactor, selectData: selectionValue, fourierN: n, type: 'lowFreq'},
            beforeSend: function(){
                $('.loader').show()
            },
            success: function(data) {
                $('#trendPlotDiv').html(data.trendPlotDiv);
                $('#trendPlotScript').html(data.trendPlotScript);
                $('#detrendValue').html(convFactor);
                $('#convolutionSlider').val(0);
                $('#convolutionValue').html(0);
                $('.loader').hide()
            },
            error: function(error){
                console.log(error);
            }
        })
    });

});

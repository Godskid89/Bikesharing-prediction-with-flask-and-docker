var weather = 'none', season=1, workingday, sliderAmount1, sliderAmount2, sliderAmount3, sliderAmount4, sliderAmount5;
var slider1, slider2, slider3, slider4, slider5;
var xaxis = [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4,30,13,12,14,15,16,14,34,67,22,23,24,25];
var yaxis;
var Weekday=0;
var Holiday=0;
var name1, name2, name3;

var temp, atemp, windspeed, humidity, hour;
var _a, _b;

[season, _a, Holiday, Weekday, workingday, weather, temp, atemp, windspeed, humidity, hour] 
= [1, 12, 0, 1, 1, 2, 0.215833, 0.223487, 0.5775, 0.154846, 0];

function myFunction(choice){

	// Seasons of the year
	if(choice == 'Summer') {
		season=2;
		$('#test1').addClass('pink');
		$('#test2').removeClass('pink');
		$('#test3').removeClass('pink');
		$('#test4').removeClass('pink');
	}
	else if (choice == 'Winter') {
		season=4
		$('#test1').removeClass('pink');
		$('#test2').addClass('pink');
		$('#test3').removeClass('pink');
		$('#test4').removeClass('pink');
	}
	else if (choice == 'Spring') {
		season=1
		$('#test1').removeClass('pink');
		$('#test2').removeClass('pink');
		$('#test3').removeClass('pink');
		$('#test4').addClass('pink');
	}
	else if (choice == 'Autumn') {
		season=3
		$('#test1').removeClass('pink');
		$('#test2').removeClass('pink');
		$('#test3').addClass('pink');
		$('#test4').removeClass('pink');
	}

	// Weather of the day
	if (choice == 'Rainy') {
		weather=4
	}
	else if (choice == 'Stormy') {
		weather=3
	}
	else if (choice == 'Sunny') {
		weather=1
	}
	else if (choice == 'Cloudy') {
		weather=2
	}

	// Weekday / Weekend / Holiday
	if (choice == 'Weekend' || choice == 'Holiday') {
		Holiday= 1 - Holiday
	}
	else if (choice == 'Weekday') {
		Weekday= 1- Weekday;
		workingday = 1 - workingday;
	}
}

// Submit to evaluate
function submit(){
	x = [635, season, 2012, 4, Holiday, Weekday, workingday, weather, temp/100, atemp/100, windspeed, humidity]
	console.log(x);
	$.ajax({
		url: '/predict',
		data: JSON.stringify({
			'data': x
		}),
		contentType: 'application/json;charset=UTF-8',
		type: 'POST',
		error: function (error) {
			console.log(error);
		},
		success: function(result){
			console.log(result);
			r = JSON.parse(result);
			$('#response').html(`Predicted Total Users: ${r['b_model']}`)
		}
	});
}

// Change value of Slider 1
function updateTemperature(sliderAmount1) {
    temp=$('#sliderDiv1').val();
    $('#temp_label').text(temp);
}

// Change value of Slider 2
function updateActualTemperature(sliderAmount2) {
    atemp=$('#sliderDiv2').val();
    $('#atemp_label').text(atemp);
}

// Change value of Slider 3
function updateWindSpeed(sliderAmount3) {
    windspeed=$('#sliderDiv3').val();
    $('#windspeed_label').text(windspeed);
}

// Change value of Slider 4
function updateHumidity(sliderAmount4) {
    humidity=$('#sliderDiv4').val();
    $('#humidity_label').text(humidity);
}


// Change value of Slider 4
function updateHour(sliderAmount4) {
    hr=$('#sliderDiv4').val();
    $('#humidity_label').text(hr);
}


function show(xaxis,yaxis){
	name1 = document.getElementById("first_name1").value;
	name2 = document.getElementById("first_name2").value;
	name3 = name2+name3;

	console.log(slider1)
	console.log(slider2)
	console.log(slider3)
	console.log(slider4)
	console.log(Holiday)
	console.log(Weekday)
	console.log(name1)
	console.log(name2)
	console.log(name3)
	draw_graph(xaxis,yaxis)
}

// Initialisation function to load all the values
function init(){
	slider1=$('#sliderDiv1').val();
	slider2=$('#sliderDiv2').val();
	slider3=$('#sliderDiv3').val();
	slider4=$('#sliderDiv4').val();
	season=1;
	weather=1;
	day=0;
}

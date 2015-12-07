var mongoose = require('mongoose');
var Yaks, Yaktags;

var Schema = mongoose.Schema,
    ObjectId = Schema.ObjectId;

 
var YakSchema = new Schema({
    author    : ObjectId,
    title     : String,
    body      : String,
    date      : Date
});


var YaktagSchema = new Schema({
	topics : Object,
	tones : Object
});



var connection = mongoose.createConnection(function(){
	var Yaks = new mongoose.model('yaks', YakSchema);
	var Yaktags = new mongoose.model('yaktags', YaktagSchema);
});


// var Yaks = new mongoose.model('yaks', YakSchema);
// var Yaktags = new mongoose.model('yaktags', YaktagSchema);


function saveModel(model){
	model.find({}, function(err,docs){

	})
}


function makegeoGrid(region){
	Yaks.
}
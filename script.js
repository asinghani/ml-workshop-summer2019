function classifyAndNext(model) {
	model.detect(video).then(pred => {
        pred = pred.map(x => x.class)
        pred = pred.filter((value, index, arr) => arr.indexOf(value) == index)

        if(pred.includes("apple")) {
            document.getElementById("overlay").src = "apple_overlay.png"
        } else if(pred.includes("banana")) {
            document.getElementById("overlay").src = "banana_overlay.png"
        }

		setTimeout(function() {
			classifyAndNext(model)
		}, 100)
	});
}

var video = document.getElementById('video');

if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
	navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: "environment" } } }).then(function(stream) {
		video.srcObject = stream;
		video.play();
	});

    cocoSsd.load().then(model => {
        classifyAndNext(model)
    });

} else{
    alert ("Camera not available")
}


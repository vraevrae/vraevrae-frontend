// create socket connection with server
let socket, user_id, quiz_id, progress_timer;

// create interval, so the progressbar can be updated every second
socket = io.connect('http://' + document.domain + ':' + location.port);

// get data from the html file
quiz_id = get_data("quiz_id");
user_id = get_data("user_id");

// if socket connected succesfully
socket.on('connect', function () {
    console.log("Socket connected");
    console.log("quiz_id ->", quiz_id);

    // join game with current quiz_id
    socket.emit('join_game', {"quiz_id": quiz_id, "user_id": user_id}); // COMMENTED BECAUSE LOBBY
    // ALREADY ADDS
    // TO QUIZ
    get_current_question(quiz_id, user_id);
});

// if socket receives a message from the server
socket.on('message', function (message) {
    console.log("SOCKET MESSAGE: ", message)
});

// if socket receives new question from the server
socket.on('current_question', function (data) {
    console.log("CURRENT QUESTION: ", data);

    // check if question is not already the current question
    if (data["question"] !== get_el("quiz-question").innerHTML) {
        // fill in template with data gotten from the server
        fill_template(quiz_id, user_id, data["question"], data["answers"])
    } else {
        console.log("ASFGDHJFKGDSA")
    }
});

// if server received answer
socket.on("received_answer", function (data) {
    data["user_id"] === user_id && updateForm(true);
    console.log("RECEIVED ANSWER", data)
});


// function to replace document.getElementById() (so code is better readable)
function get_el(id) {
    return document.getElementById(id)
}

// function to replace document.getElementById().dataset (so code is better readable)
function get_data(name) {
    return get_el("data").dataset[name]
}

// function to update timer every second
function update_timer() {
    console.log("update_timer");
    // get current progress
    let current_progress = get_el("progress_bar").value;

    // update current_progress
    current_progress -= 10;

    // set new progress
    get_el("progress_bar").value = current_progress;

    if (current_progress === 0) {
        console.log("PROGRESS === 0, NEW QUESTION");
        get_current_question();
    }

    return true
}

// function to get current question from server
function get_current_question(quiz_id = get_data("quiz_id"), user_id = get_data("user_id")) {
    console.log("GET NEW QUESTION (quiz_id, user_id)", quiz_id, user_id);
    socket.emit('get_current_question', {"quiz_id": quiz_id, "user_id": user_id});
}

// function to send answer to the server
function send_answer(answer_id, user_id = get_data("user_id", quiz_id = get_data("quiz_id"))) {
    console.log("SEND ANSWER");

    // if the button is clicked, send answer via socket to the server
    socket.emit("send_answer", {"user_id": user_id, "answer_id": answer_id, "quiz_id": quiz_id})
}

// function to update the answer buttons
function updateForm(wait = false) {
    console.log("UPDATE FORM");
    // if the user has to wait
    if (wait) {
        // update elements, so buttons can't be clicked anymore
        get_el("answer_form").style.display = "none";
        get_el("sent_answer").innerHTML = "Wait for the next question...";
    } else {
        // update elements, so buttons can be clicked
        get_el("answer_form").style.display = "block";
        get_el("sent_answer").innerHTML = "";
    }
}

// function to fill in the template
function fill_template(quiz_id, user_id, question, answers) {
    console.log("FILL TEMPLATE");
    // reset the timer
    progress_timer = setInterval(update_timer, 1000);

    get_el("quiz-question").innerHTML = question;

    // fil in the answerbuttons
    for (let i = 0; i < answers.length; i++) {
        get_el("answer-button-" + i.toString()).innerHTML = answers[i]["text"];
        get_el("answer-button-" + i.toString()).setAttribute("onclick", send_answer(answers[i]["answer_id"]));
    }
}
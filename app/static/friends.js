// connect to API to accept or decline friend requests

// add Friend
function answerFriendRequest(answer, friend_request, user, element_id) {
    console.log('running fr answer')
    fetch('/api/friendrequest', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            answer: answer,
            friend_request: friend_request,
            user: user,
        })
    }).then(response => response.json())
        .then(data => {
            console.log(data)
            if (element_id) {  // hide notifications from my_profile view. else there are no notifications
                let request_element = document.getElementById('myprofile-request-' + element_id)
                request_element.style.opacity = 0
                request_element.classList.add('resolved')

                if (document.querySelectorAll('.myprofile__request:not(.resolved)').length === 0) {
                    let requests_div = document.getElementById('myprofile-requests')
                    requests_div.style.opacity = 0
                }
            }
        })
        .catch((error) => {
            console.log(error)
        });
}


function deleteFriend(user_id, target_user) {
    fetch('/api/deletefriend', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: user_id,
            target_user: target_user,
        })
    }).then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch((error) => {
            console.log(error)
        });
}
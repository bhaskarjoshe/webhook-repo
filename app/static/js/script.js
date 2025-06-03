function formatedMessage(event){
    const {author, action, from_branch, to_branch, timestamp} = event
    if (action == "PUSH"){
        return `${author} pushed to ${to_branch} on ${timestamp}`
    }
    else if (action == "PULL_REQUEST"){
        return `${author} submitted a pull request from ${from_branch} to ${to_branch} on ${timestamp}`
    }
    else if(action == "MERGE"){
        return `${author} merged branch ${from_branch} to ${to_branch} on ${timestamp}`
    }
    else{
        return null
    }
}

async function fetchEvents(){
    const response = await fetch("/webhook/events")
    const data = await response.json()

    const container = document.getElementById("events")
    container.innerHTML = ""

    if (data.length > 0) {
        const latestLabel = document.createElement('div')
        latestLabel.classList.add('latest-label')
        latestLabel.textContent = 'Latest'
        container.appendChild(latestLabel)
    }

    data.forEach(element => {
        const message = formatedMessage(element)
        if (message){
            const div = document.createElement('div')
            div.textContent = message
            div.classList.add("event")
            container.appendChild(div)
        }
    });
}

fetchEvents()
setInterval(fetchEvents, 15000)

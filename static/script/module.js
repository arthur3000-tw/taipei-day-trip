class Order {
    constructor({price,trip,contact}){
        this.price = price
        this.trip = trip
        this.contact = contact
    }
}

class Attraction {
    constructor({id,name,address,image}){
        this.id = id
        this.name = name
        this.address = address
        this.image = image
    }
}

class Trip {
    constructor({attraction,date,time}){
        this.attraction = attraction
        this.date = date
        this.time = time
    }
}

class Contact {
    constructor({name,email,phone}){
        this.name = name
        this.email = email
        this.phone = phone
    }
}
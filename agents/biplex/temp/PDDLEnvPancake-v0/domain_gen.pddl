(define (domain pancake)

  (:requirements :strips :typing)
  (:types   
        spw - object
        apw - object
        pw - object
        wl  - object
        vpw - object
        ly  - object
        yfl - object
        tl - object
        sl - object
        yftl  - object
        syftl - object
        pwva - object
        spwva - object
        yvaftl  - object
        syvaftl - object
        vaftyu - object
        svaftyu - object
        rmcd  - c
        rmc - c
        rc -c 
        c - object
            )
  (:predicates 
        (at ?x - object)
        (inworld ?x - object)
        (have ?x - object)
        (in ?x - object ?y - c) 
    )

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;; NAVIGATION / MANIPULATION
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    (:action gofromto
    :parameters (?ob1 - object ?ob2 - object)
    :precondition (and (at ?ob1) (inworld ?ob2))
    :effect (and (not (at ?ob1)) (at ?ob2))
    )

    (:action pickup
    :parameters (?x - object)
    :precondition (and (at ?x) (inworld ?x))
    :effect (and (have ?x) (not (inworld ?x))))

    (:action putdown
    :parameters (?x - object)
    :precondition (and (have ?x))
    :effect (and (not (have ?x)) (inworld ?x)))

    (:action putin
    :parameters (?x - object ?z - c)
    :precondition (and (have ?x) (have ?z))
    :effect (and (in ?x ?z) (not (have ?x))))

    (:action takeout
    :parameters (?x - object ?z - c)
    :precondition (and (in ?x ?z) (have ?z) )
    :effect (and (not (in ?x ?z)) (inworld ?x)))
 
    (:action transfer
    :parameters (?x - object ?z1 - c ?z2 - c)
    :precondition (and (have ?z1) (have ?z2) (in ?x ?z1))
    :effect (and (in ?x ?z2) (not (in ?x ?z1)))
    )

	(:action mixeggbatter1
		:parameters (?y9b2 - yftl ?xa5c - wl ?xc8d - yfl ?x503 - tl ?z34c - rmc)
		:precondition (and (have ?xa5c) (have ?xc8d) (have ?x503) (have ?z34c))
		:effect (and (not (have ?xa5c)) (not (have ?xc8d)) (not (have ?x503)) (have ?y9b2)))
)
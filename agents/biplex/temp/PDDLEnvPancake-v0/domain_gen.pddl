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

	(:action mix1
		:parameters (?ydbf - yfl ?x98c - ly ?x636 - wftl ?x2f0 - sl ?x649 - l ?xe5f - wl ?x4f3 - ylft ?x527 - tl ?x1f3 - rmc)
		:precondition (and (have ?x98c) (have ?x636) (have ?x2f0) (have ?x649) (have ?xe5f) (have ?x4f3) (have ?x527) (have ?x1f3))
		:effect (and (not (have ?x98c)) (not (have ?x636)) (not (have ?x2f0)) (not (have ?x649)) (not (have ?xe5f)) (not (have ?x4f3)) (not (have ?x527)) (not (have ?x1f3)) (have ?ydbf)))
)
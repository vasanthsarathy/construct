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

    ;;;;;;;;;;;;;;;;;;;;;
    ;; EGG BATTER 
    ;;;;;;;;;;;;;;;;;;;;;


    ;;  yftl (eggbatter) = yfl (yoke) + tl (eggwhite) + wl (milk) in rmc (bowl)
    ;; three inputs 
    (:action hyp_mixeggbatter1
    :parameters (?y - yftl ?z - rmc)
    :precondition (and (have ?z) )
    :effect (and (have ?y)  )
    )

    ;; sugar (spw variation)
    ;; four inputs 
    (:action hyp_mixeggbatter2
    :parameters (?y - syftl  ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y) )
    )

    ;;;;;;;;;;;;;;;;;;;;;;;;
    ;; DRY INGREDIENTS
    ;;;;;;;;;;;;;;;;;;;;;;;;

    
    ;; pwva (drymix) = pw (flour) + vpw (bakingpowder) + apw (salt)
    ;; 3 inputs 
    (:action hyp_mixdryingredients1
    :parameters (?y - pwva ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y) )
    )

    ;; sugar variation 
    (:action hyp_mixdryingredients2
    :parameters (?y - spwva ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y) )
    )

    ;;;;;;;;;;;;;;;;;;;;;;;
    ;; PANCAKE BATTER 
    ;;;;;;;;;;;;;;;;;;;;;;;

    ;; yvaftl (pancakebatter) = pwva (drymix) + yftl (eggbatter)
    ;; 2 input 
    (:action hyp_mixpancakebatter1
    :parameters (?y - yvaftl ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y) )
    )

    ;; syvaftl (sweet pancakebatter)
    (:action hyp_mixpancakebatter2
    :parameters (?y - syvaftl ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y) )
    )

    (:action hyp_mixpancakebatter3
    :parameters (?y - syvaftl ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y)  )
    )

    ;; 3 inputs 
    (:action hyp_mixpancakebatter3a
    :parameters (?y - syvaftl ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y) )
    )

    (:action hyp_mixpancakebatter4
    :parameters (?y - syvaftl ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y) )
    )

    ;; 3 inputs 
    (:action hyp_mixpancakebatter4a
    :parameters (?y - syvaftl ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y)  )
    )

    (:action hyp_mixpancakebatter5
    :parameters (?y - syvaftl ?z - rmc)
    :precondition (and (have ?z))
    :effect (and (have ?y)  )
    )

    ;; 3 inputs 
    (:action hyp_mixpancakebatter5a
    :parameters (?y - syvaftl ?z - rmc)
    :precondition (and (have?z))
    :effect (and (have ?y) )
    )


    ;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;; COOK PANCAKES 
    ;;;;;;;;;;;;;;;;;;;;;;;;;;

        
    ;; vaftyu (fluffy cooked pancakes) = yvaftl (pancakebatter) + yl (oil)
    (:action hyp_cookpancake1
    :parameters (?y - vaftyu ?z - rmcd)
    :precondition (and (have ?z))
    :effect (and (have ?y)  )
    )

    (:action hyp_cookpancake2
    :parameters (?y - svaftyu ?z - rmcd)
    :precondition (and (have ?z))
    :effect (and (have ?y) )
    )

    (:action hyp_cookpancake3
    :parameters (?y - svaftyu ?z - rmcd)
    :precondition (and (have ?z))
    :effect (and (have ?y)  )
    )


    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;; DRIZZLE PANCAKES 
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    (:action hyp_drizzlepancake1
    :parameters (?y - svaftyu ?z - rc)
    :precondition (and (have ?z))
    :effect (and (have ?y)  )
    )

    (:action hyp_drizzlepancake2
    :parameters (?y - svaftyu ?z - rc)
    :precondition (and (have ?z))
    :effect (and (have ?y) )
    )

)



def TimeToBlock(turns,ores):
    pass



def enough_energy(player, energy_needed):
    need_sold_items=  0
    while(player.energy < energy_needed):
        need_sold_items += 1
        energy_needed -= 250
    return need_sold_items


def chose_action():
    energy_for_block = 250
    sold_ors = enough_energy(state.me(), energy_for_block)
    if sold_ors < 4:
        if TimeToBlock(turns_needed,4-sold_ors):
            StartBlock(sold_ors)
    
        
        
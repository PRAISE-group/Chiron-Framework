def Check_loop_in_code(src_code):
    if "repeat" in src_code:
        if "invariant" in src_code:
            return True
        else:
            raise ValueError("Error: 'repeat' statement without 'invariant' statement")    
    else:
        return False
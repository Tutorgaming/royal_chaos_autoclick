import pyautogui
import os
import time
current_path = os.path.dirname(os.path.abspath(__file__))
asset_path = current_path + "\\asset\\"


class ImageButton(object):
    """
    Do the Treasure Hunt
    """
    def __init__(self, button_name):
        self.button_img = asset_path + button_name
        

    def update_location(self):
        # Find this button 
        button_iterable = pyautogui.locateAllOnScreen(
            self.button_img
        )
        return button_iterable
    
    def find_button(self):
        button_iterable = self.update_location()
        button_findings = list(button_iterable)
        if len(button_findings) == 1:
            return True
        else:
            return False

    def find_and_click(self):
        # Search Buttons
        print "Finding : " + str(self.button_img)
        button_iterable = self.update_location()
        # Click it
        button_findings = list(button_iterable)
        if len(button_findings) == 1:
            print "Clicking : " + str(self.button_img)
            print button_findings
            pyautogui.click(button_findings[0])
            time.sleep(1)
            return True
        # Not Found
        else: 
            print "Failed : " + str(self.button_img)
            time.sleep(1)
            return False
        
class MultiStateImageButton(object):
    def __init__(self, selected, deselected):
        self.selected = ImageButton(selected)
        self.deselected = ImageButton(deselected)

    def find_and_click(self):
        print "MultiStateButton : Find Buttons"
        find_selected = self.selected.find_button()
        find_deselected = self.deselected.find_button() 
        if find_selected:
            print "MultiStateButton : Selected Found : " + str(self.selected)
            self.selected.find_and_click() 
            return True
        elif find_deselected:
            print "MultiStateButton : Deselected Found : " + str(self.selected)            
            self.deselected.find_and_click() 
            return True
        else: 
            print "MultiStateButton : Failed to find : " + str(self.selected)
            return False

class TreasureHuntAction(object):

    def __init__(self):
        print "Action : Do Treasure Hunt 3 times"
        self.action()
    
    def do_treasure_hunt(self):
        do_treasure = ImageButton("treasure_button.png")
        do_treasure.find_and_click()
  
        do_treasure_unlock = ImageButton("treasure_unlock.png")
        result = do_treasure_unlock.find_and_click()

        # Constrain already satisfy 
        if not result:
            # Find Speed Up Banner 
            do_speed_up = ImageButton("speed_up.png")
            do_speed_up.find_and_click()
            # Get out Speed Up
            do_speed_up_exit = ImageButton("speed_up_exit.png")
            do_speed_up_exit.find_and_click() 
            print "Already Travel - Travel Power Off"
            return True
        # Clear Treasure Screen
        do_treasure_complete = ImageButton("treasure_opened.png")
        do_treasure_complete.find_and_click()

    def action(self):
        for idx in range(3):
            result = self.do_treasure_hunt()
            if result is False:
                print "Action : Treasure Hunt : Failed "
            time.sleep(1)
        print "Action : Treasure Hunt : Complete"

class GoToExploreTabAction(object):
    def __init__(self):
        print "Action : Go to Explore Tab"
        self.action()

    def action(self):
        explore_tab = MultiStateImageButton(
            "tab_explore_selected.png",
            "tab_explore_deselected.png"
        )
        explore_tab.find_and_click()
        time.sleep(2)

class GoToBattleTabAction(object):
    def __init__(self):
        print "Action : Go to Battle(Main) Tab"
        self.action()
        
    def action(self):
        battle_tab = MultiStateImageButton(
            "tab_battle_selected.png",
            "tab_battle_deselected.png"
        )
        battle_tab.find_and_click()
        time.sleep(2)

class GoToBiographyLandmark(object):
    def __init__(self):
        print "Action : Go To Biography Landmark"
        self.action() 

    def action(self):
        go_landmark_biography = ImageButton("landmark_biography.png")
        result = go_landmark_biography.find_and_click()
        time.sleep(2)

class DoBioGraphyPanAn(object):
    def __init__(self):
        print "Action : Do Biography Pan-an"
        self.action() 

    def select_pan_an(self):
        do_panan = ImageButton("biography_panan.png")
        result = do_panan.find_and_click()
        return result

    def select_difficulty(self):
        do_select_6 = MultiStateImageButton(
            "biography_level_6_selected.png",
            "biography_level_6_deselected.png"
        )
        result = do_select_6.find_and_click()
        return result

    def do_challenge(self):
        do_challenge = ImageButton("biography_challenge.png")
        result = do_challenge.find_and_click()
        return result
    
    def do_enter_fight(self):
        do_fight = ImageButton("biography_do_fight.png")
        result = do_fight.find_and_click()
        return result

    def do_skip(self):
        skip = ImageButton("biography_skip.png")
        result = skip.find_and_click()
        return result

    def action(self):
        self.select_pan_an()
        result = self.select_difficulty()
        if result:
            self.do_challenge()
            self.do_enter_fight()
            time.sleep(6)
            # Must Wait For Fight Scene
            self.do_skip()
            # Clear Treasure Screen
            do_treasure_complete = ImageButton("treasure_opened.png")
            do_treasure_complete.find_and_click()

        time.sleep(1)

def main():
    # Always Start at Battle Tab 
    go_battle_tab = GoToBattleTabAction()
    # # Treasure Hunt 3 Times 
    # treasure_hunt = TreasureHuntAction()
    # go_battle_tab = GoToBattleTabAction()
    # Go Explore Tab
    go_explore_tab = GoToExploreTabAction()
    # Go Biography
    go_biography = GoToBiographyLandmark()
    # Do Panan
    pan_an_biography = DoBioGraphyPanAn()
   
if __name__ == "__main__":
    main()

import ac
import acsys

app_dash = 0
app_pedals = 0
app_settings = 0

label_speed = 0
label_gear = 0

MAX_RPM = 7500
MAX_SPEED = 250

SCALE_DASH = 0.8
SCALE_PEDALS = 0.7

previous_gear = 1
clutch_timer = 0.0


def napravi_cisti_prozor(ime, width, height):
    app = ac.newApp(ime)
    ac.setSize(app, width, height)
    ac.setBackgroundOpacity(app, 0.0)
    ac.drawBorder(app, 0)
    ac.setTitle(app, "")
    ac.setIconPosition(app, -10000, -10000)
    return app


def acMain(ac_version):
    global app_dash, app_pedals, app_settings, label_speed, label_gear

    # Glavni Dashboard
    app_dash = napravi_cisti_prozor("KB Dash", int(300 * SCALE_DASH), int(160 * SCALE_DASH))

    label_speed = ac.addLabel(app_dash, "0 km/h")
    ac.setPosition(label_speed, 15, 15)
    ac.setFontSize(label_speed, int(28 * SCALE_DASH))

    label_gear = ac.addLabel(app_dash, "N")
    ac.setPosition(label_gear, int(250 * SCALE_DASH), 15)
    ac.setFontSize(label_gear, int(28 * SCALE_DASH))

    ac.addRenderCallback(app_dash, onRenderDash)

    #  Pedale
    app_pedals = napravi_cisti_prozor("KB Pedals", int(130 * SCALE_PEDALS), int(170 * SCALE_PEDALS))
    ac.addRenderCallback(app_pedals, onRenderPedals)

    # PROZOR ZA POSTAVKE
    app_settings = ac.newApp("KB Settings")
    ac.setSize(app_settings, 230, 110)
    ac.setBackgroundOpacity(app_settings, 0.85)
    ac.setTitle(app_settings, "KB Settings")

    # Dash kontrole
    lbl_d = ac.addLabel(app_settings, "Dash Velicina:")
    ac.setPosition(lbl_d, 15, 15)

    btn_dash_plus = ac.addButton(app_settings, "+")
    ac.setPosition(btn_dash_plus, 130, 12)
    ac.setSize(btn_dash_plus, 40, 25)
    ac.addOnClicked(btn_dash_plus, dash_povecaj)

    btn_dash_minus = ac.addButton(app_settings, "-")
    ac.setPosition(btn_dash_minus, 175, 12)
    ac.setSize(btn_dash_minus, 40, 25)
    ac.addOnClicked(btn_dash_minus, dash_smanji)

    # Pedale kontrole
    lbl_p = ac.addLabel(app_settings, "Pedale Velicina:")
    ac.setPosition(lbl_p, 15, 60)

    btn_ped_plus = ac.addButton(app_settings, "+")
    ac.setPosition(btn_ped_plus, 130, 57)
    ac.setSize(btn_ped_plus, 40, 25)
    ac.addOnClicked(btn_ped_plus, pedals_povecaj)

    btn_ped_minus = ac.addButton(app_settings, "-")
    ac.setPosition(btn_ped_minus, 175, 57)
    ac.setSize(btn_ped_minus, 40, 25)
    ac.addOnClicked(btn_ped_minus, pedals_smanji)

    return "KB Telemetry"


def primijeni_skalu_dash():
    """Prilagodi velicinu prozora i fontove trenutnoj skali."""
    ac.setSize(app_dash, int(300 * SCALE_DASH), int(160 * SCALE_DASH))
    ac.setFontSize(label_speed, int(28 * SCALE_DASH))
    ac.setFontSize(label_gear, int(28 * SCALE_DASH))
    ac.setPosition(label_gear, int(250 * SCALE_DASH), 15)


def primijeni_skalu_pedals():
    ac.setSize(app_pedals, int(130 * SCALE_PEDALS), int(170 * SCALE_PEDALS))


def dash_povecaj(unity, value):
    global SCALE_DASH
    SCALE_DASH = min(2.0, SCALE_DASH + 0.1)
    primijeni_skalu_dash()


def dash_smanji(unity, value):
    global SCALE_DASH
    SCALE_DASH = max(0.5, SCALE_DASH - 0.1)
    primijeni_skalu_dash()


def pedals_povecaj(unity, value):
    global SCALE_PEDALS
    SCALE_PEDALS = min(2.0, SCALE_PEDALS + 0.1)
    primijeni_skalu_pedals()


def pedals_smanji(unity, value):
    global SCALE_PEDALS
    SCALE_PEDALS = max(0.5, SCALE_PEDALS - 0.1)
    primijeni_skalu_pedals()


def acUpdate(deltaT):
    pass


def onRenderDash(deltaT):
    global MAX_RPM, MAX_SPEED, SCALE_DASH, label_speed, label_gear

    rpm = ac.getCarState(0, acsys.CS.RPM)
    speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    steer = ac.getCarState(0, acsys.CS.Steer)

    gear = ac.getCarState(0, acsys.CS.Gear) - 1

    if gear == -1:
        gear_text = "R"
    elif gear == 0:
        gear_text = "N"
    else:
        gear_text = str(gear)

    ac.setText(label_speed, "{:.0f}".format(speed))
    ac.setText(label_gear, gear_text)

    bar_max_width = int(270 * SCALE_DASH)

    # Brzina bar
    speed_pct = min(speed / MAX_SPEED, 1.0)
    ac.glColor4f(0.3, 0.3, 0.3, 0.5)
    ac.glQuad(15, int(60 * SCALE_DASH), bar_max_width, int(10 * SCALE_DASH))
    ac.glColor4f(1.0, 1.0, 1.0, 0.8)
    ac.glQuad(15, int(60 * SCALE_DASH), int(bar_max_width * speed_pct), int(10 * SCALE_DASH))

    # RPM bar
    rpm_pct = min(rpm / MAX_RPM, 1.0)
    ac.glColor4f(0.3, 0.3, 0.3, 0.5)
    ac.glQuad(15, int(80 * SCALE_DASH), bar_max_width, int(20 * SCALE_DASH))

    if rpm_pct > 0.85:
        ac.glColor4f(1.0, 0.1, 0.1, 1.0)
    elif rpm_pct > 0.60:
        ac.glColor4f(1.0, 0.8, 0.1, 1.0)
    else:
        ac.glColor4f(0.1, 0.8, 1.0, 1.0)
    ac.glQuad(15, int(80 * SCALE_DASH), int(bar_max_width * rpm_pct), int(20 * SCALE_DASH))

    # Volan
    steer_pct = max(-1.0, min(1.0, steer / 450.0))
    center_x = 15 + (bar_max_width / 2)
    steer_width = abs(steer_pct * (bar_max_width / 2))

    ac.glColor4f(0.2, 0.2, 0.2, 0.6)
    ac.glQuad(15, int(120 * SCALE_DASH), bar_max_width, int(15 * SCALE_DASH))

    ac.glColor4f(0.0, 0.7, 1.0, 0.9)
    if steer_pct < 0:
        ac.glQuad(int(center_x - steer_width), int(120 * SCALE_DASH), int(steer_width), int(15 * SCALE_DASH))
    else:
        ac.glQuad(int(center_x), int(120 * SCALE_DASH), int(steer_width), int(15 * SCALE_DASH))

    ac.glColor4f(1.0, 0.0, 0.0, 1.0)
    ac.glQuad(int(center_x - 1), int(115 * SCALE_DASH), int(2 * SCALE_DASH), int(25 * SCALE_DASH))


def onRenderPedals(deltaT):
    global SCALE_PEDALS, previous_gear, clutch_timer

    gas = ac.getCarState(0, acsys.CS.Gas)
    brake = ac.getCarState(0, acsys.CS.Brake)
    current_gear = ac.getCarState(0, acsys.CS.Gear)

    if current_gear != previous_gear:
        previous_gear = current_gear
        clutch_timer = 0.2

    if clutch_timer > 0:
        clutch_timer -= deltaT
        clutch = 1.0
    else:
        clutch = 0.0

    max_h = int(140 * SCALE_PEDALS)
    base_y = int(155 * SCALE_PEDALS)
    w = int(25 * SCALE_PEDALS)
    gap = int(35 * SCALE_PEDALS)

    ac.glColor4f(0.2, 0.2, 0.2, 0.4)
    ac.glQuad(15, base_y - max_h, w, max_h)
    ac.glQuad(15 + gap, base_y - max_h, w, max_h)
    ac.glQuad(15 + (gap * 2), base_y - max_h, w, max_h)

    c_h = int(max_h * clutch)
    ac.glColor4f(1.0, 0.9, 0.0, 0.9)
    ac.glQuad(15, base_y - c_h, w, c_h)

    b_h = int(max_h * brake)
    ac.glColor4f(1.0, 0.0, 0.0, 0.9)
    ac.glQuad(15 + gap, base_y - b_h, w, b_h)

    g_h = int(max_h * gas)
    ac.glColor4f(0.0, 1.0, 0.0, 0.9)
    ac.glQuad(15 + (gap * 2), base_y - g_h, w, g_h)
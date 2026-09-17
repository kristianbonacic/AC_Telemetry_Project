import ac
import acsys

app_dash = 0
app_pedals = 0
app_settings = 0

label_speed = 0
label_unit = 0
label_gear = 0

label_ped_c = 0
label_ped_b = 0
label_ped_g = 0

MAX_RPM = 7500
MAX_SPEED = 250

SCALE_DASH = 0.8
SCALE_PEDALS = 0.7

DASH_W = 340
DASH_H = 175

PED_W = 150
PED_H = 195

RPM_SEGMENTI = 24

previous_gear = 1
clutch_timer = 0.0

blink_timer = 0.0


def napravi_cisti_prozor(ime, width, height):
    app = ac.newApp(ime)
    ac.setSize(app, width, height)
    ac.setBackgroundOpacity(app, 0.0)
    ac.drawBorder(app, 0)
    ac.setTitle(app, "")
    ac.setIconPosition(app, -10000, -10000)
    return app


def panel(x, y, w, h, r, g, b, a):
    """Pomocna funkcija za crtanje pozadinske plohe."""
    ac.glColor4f(r, g, b, a)
    ac.glQuad(int(x), int(y), int(w), int(h))


def acMain(ac_version):
    global app_dash, app_pedals, app_settings
    global label_speed, label_unit, label_gear
    global label_ped_c, label_ped_b, label_ped_g

    # 1. Glavni Dashboard
    app_dash = napravi_cisti_prozor("KB Dash", int(DASH_W * SCALE_DASH), int(DASH_H * SCALE_DASH))

    label_speed = ac.addLabel(app_dash, "0")
    label_unit = ac.addLabel(app_dash, "km/h")
    label_gear = ac.addLabel(app_dash, "N")

    ac.addRenderCallback(app_dash, onRenderDash)

    # 2. Pedale
    app_pedals = napravi_cisti_prozor("KB Pedals", int(PED_W * SCALE_PEDALS), int(PED_H * SCALE_PEDALS))

    label_ped_c = ac.addLabel(app_pedals, "C")
    label_ped_b = ac.addLabel(app_pedals, "B")
    label_ped_g = ac.addLabel(app_pedals, "G")

    ac.addRenderCallback(app_pedals, onRenderPedals)

    primijeni_skalu_dash()
    primijeni_skalu_pedals()

    # 3. PROZOR ZA POSTAVKE
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
    """Velicina prozora, pozicije i fontovi prate SCALE_DASH."""
    s = SCALE_DASH
    ac.setSize(app_dash, int(DASH_W * s), int(DASH_H * s))

    ac.setPosition(label_speed, int(20 * s), int(12 * s))
    ac.setFontSize(label_speed, int(40 * s))
    ac.setFontAlignment(label_speed, "left")
    ac.setFontColor(label_speed, 1.0, 1.0, 1.0, 1.0)


    ac.setPosition(label_unit, int(22 * s), int(58 * s))
    ac.setFontSize(label_unit, int(14 * s))
    ac.setFontAlignment(label_unit, "left")
    ac.setFontColor(label_unit, 0.55, 0.6, 0.65, 1.0)


    ac.setPosition(label_gear, int((DASH_W - 22) * s), int(8 * s))
    ac.setFontSize(label_gear, int(48 * s))
    ac.setFontAlignment(label_gear, "right")


def primijeni_skalu_pedals():
    s = SCALE_PEDALS
    ac.setSize(app_pedals, int(PED_W * s), int(PED_H * s))

    y = int(163 * s)
    font = int(13 * s)

    for lbl, x in ((label_ped_c, 33), (label_ped_b, 73), (label_ped_g, 113)):
        ac.setPosition(lbl, int(x * s), y)
        ac.setFontSize(lbl, font)
        ac.setFontAlignment(lbl, "center")
        ac.setFontColor(lbl, 0.55, 0.6, 0.65, 1.0)


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
    global blink_timer

    s = SCALE_DASH
    rpm = ac.getCarState(0, acsys.CS.RPM)
    speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    steer = ac.getCarState(0, acsys.CS.Steer)
    gear = ac.getCarState(0, acsys.CS.Gear) - 1

    rpm_pct = min(rpm / MAX_RPM, 1.0)
    speed_pct = min(speed / MAX_SPEED, 1.0)

    blink_timer += deltaT
    if blink_timer > 1000.0:
        blink_timer = 0.0
    blink_on = (blink_timer % 0.16) < 0.08

    panel(0, 0, DASH_W * s, DASH_H * s, 0.05, 0.06, 0.08, 0.72)
    panel(0, 0, DASH_W * s, 3 * s, 0.0, 0.7, 1.0, 0.9)

    ac.setText(label_speed, "{:.0f}".format(speed))

    if gear == -1:
        gear_text = "R"
        ac.setFontColor(label_gear, 1.0, 0.45, 0.2, 1.0)
    elif gear == 0:
        gear_text = "N"
        ac.setFontColor(label_gear, 0.55, 0.6, 0.65, 1.0)
    else:
        gear_text = str(gear)
        if rpm_pct > 0.92 and blink_on:
            ac.setFontColor(label_gear, 1.0, 0.15, 0.15, 1.0)
        else:
            ac.setFontColor(label_gear, 1.0, 1.0, 1.0, 1.0)

    ac.setText(label_gear, gear_text)

    # RPM 
    rpm_y = 90 * s
    rpm_h = 16 * s
    traka_x = 20 * s
    traka_w = (DASH_W - 40) * s

    gap = 2 * s
    seg_w = (traka_w - gap * (RPM_SEGMENTI - 1)) / RPM_SEGMENTI
    aktivni = int(rpm_pct * RPM_SEGMENTI)

    for i in range(RPM_SEGMENTI):
        x = traka_x + i * (seg_w + gap)
        udio = float(i) / RPM_SEGMENTI

        if i < aktivni:
            if rpm_pct > 0.92 and blink_on:
                ac.glColor4f(1.0, 1.0, 1.0, 1.0)
            elif udio > 0.85:
                ac.glColor4f(1.0, 0.15, 0.15, 1.0)
            elif udio > 0.60:
                ac.glColor4f(1.0, 0.75, 0.1, 1.0)
            else:
                ac.glColor4f(0.1, 0.8, 1.0, 1.0)
        else:
            ac.glColor4f(1.0, 1.0, 1.0, 0.08)

        ac.glQuad(int(x), int(rpm_y), int(seg_w) + 1, int(rpm_h))

    #Brzina
    sp_y = 118 * s
    sp_h = 5 * s
    panel(traka_x, sp_y, traka_w, sp_h, 1.0, 1.0, 1.0, 0.08)
    panel(traka_x, sp_y, traka_w * speed_pct, sp_h, 0.9, 0.92, 0.95, 0.85)

    # Volan
    st_y = 138 * s
    st_h = 9 * s
    steer_pct = max(-1.0, min(1.0, steer / 450.0))
    center_x = traka_x + traka_w / 2.0
    steer_w = abs(steer_pct) * (traka_w / 2.0)

    panel(traka_x, st_y, traka_w, st_h, 1.0, 1.0, 1.0, 0.08)

    ac.glColor4f(0.0, 0.7, 1.0, 0.9)
    if steer_pct < 0:
        ac.glQuad(int(center_x - steer_w), int(st_y), int(steer_w), int(st_h))
    else:
        ac.glQuad(int(center_x), int(st_y), int(steer_w), int(st_h))

    
    panel(center_x - 1 * s, st_y - 3 * s, 2 * s, st_h + 6 * s, 1.0, 1.0, 1.0, 0.55)


def onRenderPedals(deltaT):
    global previous_gear, clutch_timer

    s = SCALE_PEDALS
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

    #Pozadina
    panel(0, 0, PED_W * s, PED_H * s, 0.05, 0.06, 0.08, 0.72)
    panel(0, 0, PED_W * s, 3 * s, 0.0, 0.7, 1.0, 0.9)

    max_h = 130 * s
    base_y = 155 * s
    w = 26 * s
    gap = 40 * s
    x0 = 20 * s

    podaci = (
        (clutch, 1.0, 0.9, 0.0),
        (brake, 1.0, 0.2, 0.2),
        (gas, 0.2, 1.0, 0.4),
    )

    for i, (vrijednost, r, g, b) in enumerate(podaci):
        x = x0 + i * gap

        
        panel(x, base_y - max_h, w, max_h, 1.0, 1.0, 1.0, 0.07)

        h = max_h * vrijednost
        if h > 0:
            panel(x, base_y - h, w, h, r, g, b, 0.9)
            panel(x, base_y - h, w, 2 * s, 1.0, 1.0, 1.0, 0.6)

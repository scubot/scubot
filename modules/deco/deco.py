from modules.botModule import BotModule
from modules.deco.algorithm import DecoAlgorithm, meter_to_bar, bar_to_meter
import shlex

class Deco(BotModule):
    name = 'deco'  # name of your module

    description = 'This module preforms decompression calculations using the Buehlmann ZH-16 decompression algorithm ' \
                  'with gradient factors(30,80 by default)'  # description of its function

    help_text = "G              :   Adds a gas to the gas list, takes the form of G<FrN2>:<FrO2>:<FrHe>,\n" \
                "                   air (expressed as G0.21:0.79:0) is automatically added as the zeroth element\n" \
                "                   and gases can be accessed in the order they are added.\n" \
                "D              :   Add depths and times to the model, takes the form D<Depth1>,<Time1>:<Depth2>,<Time2>...\n" \
                "                   For example a dive that goes to 10 meters for 10 minutes then goes to 60 meters for 5 minutes\n" \
                "                   would be expressed as D10,10:60,5"  # help text for explaining how to do things

    trigger_string = '!deco'  # string to listen for as trigger

    has_background_loop = False  # start background loop

    module_version = '0.0.1'  # version of the current module

    async def parse_command(self, message, client):
        deco_actual = DecoAlgorithm()
        msg = shlex.split(message.content)
        for i in msg:
            if i.startswith('GFL'):
                deco_actual.GFLow = float(i.replace('GFL', ''))
            elif i.startswith('GFH'):
                deco_actual.GFHigh = float(i.replace('GFH', ''))
            elif i.startswith('G'):
                parameters = i.replace('G', '').split('/')
                fr_n2 = float(parameters[0])
                fr_he = float(parameters[1])
                deco_actual.create_gas(fr_n2, fr_he)
            elif i.startswith('D'):
                parameters = i.replace('D', '').split(':')
                for j in parameters:
                    depths = j.split(',')
                    depth = float(depths[0])
                    time = float(depths[1])
                    deco_actual.add_decent(meter_to_bar(depth), meter_to_bar(deco_actual.DecentRate))
                    deco_actual.add_bottom(time)
        if bar_to_meter(deco_actual.get_ceiling()) > 0:
            schedule = deco_actual.get_deco_schedule()
            for i in range(len(schedule)):
                await client.send_message(message.channel,
                                          "Deco Depth(" + str(i) + "): " + str(bar_to_meter(schedule[i].Depth)))
                await client.send_message(message.channel, "Deco time(" + str(i) + "): " + str(schedule[i].Time))
        else:
            await client.send_message(message.channel, "Remaining No Stop Time: " + str(deco_actual.get_no_deco_time()))

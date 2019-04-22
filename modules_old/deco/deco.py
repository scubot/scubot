from modules_old.botModule import BotModule
from modules_old.deco.algorithm import *
import shlex


class Deco(BotModule):
    name = 'deco'  # name of your module

    description = 'This module preforms decompression calculations using the Bühlmann ZHL-16C decompression algorithm ' \
                  'with gradient factors(30,80 by default)'  # description of its function

    help_text = "G : Adds a gas to the gas list, takes the form of G<FrN2>/<FrHe>," \
                "air (expressed as G0.79/0) is automatically added the default gas." \
                " Gas switching has yet to be implemented.\n\n" \
                "D : Add depths and times to the model, takes the form D<Depth1>,<Time1>:<Depth2>,<Time2>... " \
                "For example a dive that goes to 10 meters for 10 minutes then goes to 60 meters for 5 minutes" \
                " would be expressed as D10,10:60,5\n\n" \
                "GFL : Sets the low percentage for gradient factors (e.g. GFL30 will set the low gradient factor to" \
                " 30%\n\n" \
                "GFH : Sets the high percentage for gradient factors (e.g. GFH80 will set the high gradient factor to" \
                " 80%\n\n"  # help text for explaining how to do things

    trigger_string = 'deco'  # string to listen for as trigger

    has_background_loop = False  # start background loop

    module_version = '1.1.0'  # version of the current module

    async def parse_command(self, message, client):
        message_string = '**This algorithm is a prototype and has known issues, not for actual dive planning!**\n\n'
        deco_actual = DecoAlgorithm()
        msg = shlex.split(message.content)
        for i in msg:
            if i.startswith('GFL'):
                try:
                    deco_actual.GFLow = float(i.replace('GFL', '')) / 100  # Divide by 100 to make decimal form
                except:
                    await client.send_message(message.channel, 'Invalid parameter for GFL')
                    return
            elif i.startswith('GFH'):
                try:
                    deco_actual.GFHigh = float(i.replace('GFH', '')) / 100  # Divide by 100 to make decimal form
                except:
                    await client.send_message(message.channel, 'Invalid parameter for GFH')
                    return
            elif i.startswith('G'):
                try:
                    parameters = i.replace('G', '').split('/')
                    fr_n2 = float(parameters[0])
                    fr_he = float(parameters[1])
                    deco_actual.create_gas(fr_n2, fr_he)
                except:
                    await client.send_message(message.channel, 'Invalid parameter for Gas')
                    return
            elif i.startswith('D'):
                try:
                    parameters = i.replace('D', '').split(':')
                    for j in parameters:
                        depths = j.split(',')
                        depth = float(depths[0])
                        time = float(depths[1])
                        deco_actual.add_decent(meter_to_bar(depth), meter_to_bar(deco_actual.DecentRate))
                        deco_actual.add_bottom(time)
                except:
                    await client.send_message(message.channel, 'Invalid parameter for Dive Profile')
                    return
        if deco_actual.get_ceiling() > 1:
            schedule = deco_actual.get_deco_schedule()
            time_to_surface = 0
            for i in range(len(schedule)):
                message_string += "Deco Depth (" + str(i) + "): " + \
                                  str("{0:.2f}".format(math.floor(bar_to_meter(schedule[i].Depth)))) + ' meters \n'

                message_string += "Deco time (" + str(i) + "): " + \
                                  str("{0:.2f}".format(math.ceil(schedule[i].Time))) + ' min\n\n'
                time_to_surface += schedule[i].Time
            message_string += "Time to surface: " + str("{0:.2f}".format(math.ceil(time_to_surface))) + " min"

        else:
            message_string += "Remaining No Stop Time: " + str(math.ceil(deco_actual.get_no_deco_time())) + " min"
        await client.send_message(message.channel, message_string)

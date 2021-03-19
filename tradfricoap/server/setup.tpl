<HEAD>
    <title>Test Form</title>
</HEAD>

<h2>Configure Tradfri</h2>
<form name="config" action="/setup" method="POST">
    <table>
        <tr>
                    
        <td style="text-align:right"><label for="tradfri-ip">IP:</label></td>
        <td><input type="text" id="tradfri-ip" name="tradfri-ip" style="width: 250px; padding: .2em;" class="text ui-widget-content ui-corner-all"></td>
        </tr>
        <tr>       
        <td style="text-align:right"><label for="tradfri-key">Key:</label></td>
        <td><input type="text" id="tradfri-key" name="tradfri-key" style="width: 250px; padding: .2em;" class="text ui-widget-content ui-corner-all"></td>
        </tr> 
        <tr> <td colspan="2" style="text-align:right"><input class="btnstyle3" type="submit" value="Apply"></td></tr>
    </table>
</form>
import datetime


def pass_fail(attackResult):
    return attackResult.result


def summary(results):
    pass_count = 0
    fail_count = 0
    for attackResult in results:
        value = attackResult.result
        if value:
            pass_count += 1
        else:
            fail_count += 1

    return {'pass': pass_count, 'fail': fail_count, 'total': pass_count + fail_count}


def console(sorted_results):
    for result in sorted_results:
        if not result.result:
            print('\u001b[31m' + str(result))
        else:
            print('\u001b[32m' + str(result))


def html(root_dir, results):
    f = open(root_dir + 'attack_output.html', 'w')
    summary_results = summary(results)

    f.write('<html>\n<head>\n')
    f.write('<script>\n')
    f.write('  function expandCollapse(event) {\n')
    f.write('    event.nextElementSibling.classList = event.nextElementSibling.classList == \"hide\" ? \"show\" : \"hide\";\n')
    f.write('  }\n')
    f.write('  function mouseOver(event) {\n')
    f.write('    event.style.background = event.style.background == \"khaki\" ? \"white\" : \"khaki\";\n')
    f.write('  }\n')
    f.write('</script>\n')
    f.write('<style>\n')
    f.write('  table, tr, th, td {\n')
    f.write('    padding: 5px;\n')
    f.write('    border: 1px solid black;\n')
    f.write('  }\n')
    f.write('  table {\n')
    f.write('    width: 100%;\n')
    f.write('    border-collapse: collapse;\n')
    f.write('  }\n')
    f.write('  [data-result="Fail"] {\n')
    f.write('    background: #EC7063;\n')
    f.write('  }\n')
    f.write('  [data-result="Pass"] {\n')
    f.write('    background: #76D7C4;\n')
    f.write('  }\n')
    f.write('  [data-result="Total"] {\n')
    f.write('    background: khaki;\n')
    f.write('  }\n')
    f.write('  .hide {\n')
    f.write('    display: none;\n')
    f.write('  }\n')
    f.write('</style>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<h2>Automated Security Test Report</h2>\n')

    f.write('<table>\n')
    f.write('<tr>\n')
    f.write('<th>Pass</th>\n')
    f.write('<th>Fail</th>\n')
    f.write('<th>Total</th>\n')
    f.write('</tr>\n')
    f.write('<tr>\n')
    f.write('<td data-result=\"Pass\">{}</td>\n'.format(str(summary_results['pass'])))
    f.write('<td data-result=\"Fail\">{}</td>\n'.format(str(summary_results['fail'])))
    f.write('<td data-result=\"Total\">{}</td>\n'.format(str(summary_results['total'])))
    f.write('</tr>\n')
    f.write('</table>\n')
    f.write('<br>\n')

    f.write('<table>\n')
    f.write('<tr>\n')
    f.write('<th align=\"left\">Attack</th>\n')
    f.write('<th align=\"left\">Result</th>\n')
    f.write('<th align=\"left\">Context</th>\n')
    f.write('</tr>\n')

    for attackResult in results:
        pass_fail_text = 'Fail'
        if attackResult.result:
            pass_fail_text = 'Pass'

        f.write('<tr onmouseover=\"mouseOver(this)\" onmouseout=\"mouseOver(this)\" onclick=\"expandCollapse(this)\">\n')
        f.write('<td>{}</td><td data-result={}>{}</td><td>{}</td>\n'.format(attackResult.attack,
                                                                            pass_fail_text,
                                                                            pass_fail_text,
                                                                            attackResult.context))
        f.write('</tr>\n')

        f.write('<tr class=\"hide\">\n')
        f.write('<td colspan=3>{}</td>\n'.format(attackResult.details))
        f.write('</tr>\n')

    f.write('</table>\n')
    f.write('<br>Attacked: ' + str(datetime.datetime.now()))
    f.write('</body>\n</html>\n')
    f.close()

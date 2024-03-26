import tabulate

class Template:
    
    def __init__(self) -> None:
        pass
        
    def MessageHTML(self,title):
        title = f'<b>{title}</b>\n'
        return title
    
    def MessageMarkdown(self,title):
        title = f'*{title}*\n'
        return title
    
    def TableHTML(self,name_cols,data):
        table = f'<div style="background-color: aliceblue;>'
        table += f'<table class="table"><tbody>'
        table += f'<tr>'
        for name in name_cols:
            table += f'<td><strong>{name}</strong></td>'
        table += f'</tr>'
        for row in range(len(data)):
            table += f'<tr>'
            for name in name_cols:
                table += f'<td>{data[row][name]}</td>' 
            table += f'</tr>'
        table += f'</tbody></table>'
        table += f'</div>'
        
        return table
    
    def TableMarkdown(self,data):
        
        table = tabulate.tabulate(data,headers="keys",tablefmt="pipe")
        return table
    
    def LogsourcesMessage(self,data):
        
        msg = ""
        for eps_log in data:
            msg += f'{eps_log["LogSource Name"]} : {eps_log["EPS"]}\n'
        return msg
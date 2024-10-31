class Logger:
    def __init__(self):
        self.messages = []
        self.alerts = []
        self.errors = []
        self.output = ""
    
    def log(self, msg):
        self.messages.append(msg)
    
    def warning(self, msg):
        self.alerts.append(msg)
    
    def error(self, msg):
        self.errors.append(msg)
        
    def display(self):
        if self.messages:
            for msg in self.messages:
                self.output += f"{msg}; "
        if self.errors:
            self.out("Errors", self.errors)
        if self.alerts:
            self.out("Warnings", self.alerts)
        print(self.output)

    def out(self, type, messages):
        if self.messages or self.alerts:
            self.output += "--------- "
        self.output += f"**{type}** "
        for i, msg in enumerate(messages):
            self.output += f"{i + 1}.{msg}; "
    
    def merge(self, logger):
        self.messages.extend(logger.messages)
        self.alerts.extend(logger.alerts)
        self.errors.extend(logger.errors)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def base_data(data):
    X_win = (data[['winning_mag', 'winning_phy', 'winning_mit']]
            .rename(columns={'winning_mag':'mag', 'winning_phy':'phy', 'winning_mit':'mit'}))
    X_loss = (data[['losing_mag', 'losing_phy', 'losing_mit']]
            .rename(columns={'losing_mag':'mag', 'losing_phy':'phy', 'losing_mit':'mit'}))
    return X_win, X_loss

def mp_data(data):
    X_win = (data[['winning_mag', 'winning_phy', 'winning_mit', 'winning_magphy']]
            .rename(columns={'winning_mag':'mag', 'winning_phy':'phy', 'winning_mit':'mit', 'winning_magphy':'magphy'}))
    X_loss = (data[['losing_mag', 'losing_phy', 'losing_mit', 'losing_phymit']]
            .rename(columns={'losing_mag':'mag', 'losing_phy':'phy', 'losing_mit':'mit', 'losing_magphy':'magphy',}))
    return X_win, X_loss

def pm_data(data):
    X_win = (data[['winning_mag', 'winning_phy', 'winning_mit', 'winning_phymit']]
            .rename(columns={'winning_mag':'mag', 'winning_phy':'phy', 'winning_mit':'mit', 'winning_phymit':'phymit'}))
    X_loss = (data[['losing_mag', 'losing_phy', 'losing_mit', 'losing_phymit']]
            .rename(columns={'losing_mag':'mag', 'losing_phy':'phy', 'losing_mit':'mit', 'losing_phymit':'phymit',}))
    return X_win, X_loss

def mpm_data(data):
    X_win = (data[['winning_mag', 'winning_phy', 'winning_mit', 'winning_magphymit']]
            .rename(columns={'winning_mag':'mag', 'winning_phy':'phy', 'winning_mit':'mit', 'winning_magphymit':'magphymit'}))
    X_loss = (data[['losing_mag', 'losing_phy', 'losing_mit', 'losing_magphymit']]
            .rename(columns={'losing_mag':'mag', 'losing_phy':'phy', 'losing_mit':'mit', 'losing_magphymit':'magphymit'}))
    return X_win, X_loss

def all_data(data):
    X_win = (data[['winning_mag', 'winning_phy', 'winning_mit', 'winning_magphy', 'winning_phymit', 'winning_magphymit']]
            .rename(columns={'winning_mag':'mag', 'winning_phy':'phy', 'winning_mit':'mit', 'winning_magphy':'magphy', 'winning_phymit':'phymit', 'winning_magphymit':'magphymit'}))
    X_loss = (data[['losing_mag', 'losing_phy', 'losing_mit', 'losing_magphy', 'losing_phymit', 'losing_magphymit']]
            .rename(columns={'losing_mag':'mag', 'losing_phy':'phy', 'losing_mit':'mit', 'losing_magphy':'magphy', 'losing_phymit':'phymit', 'losing_magphymit':'magphymit'}))
    return X_win, X_loss
    
def get_data(file, mode='base'):
    # read raw data from csv
    data = pd.read_csv(file)

    mode_to_func = {'base':base_data, 'mp':mp_data, 'pm':pm_data, 'mpm':mpm_data, 'all':all_data}
    func = mode_to_func[mode]

    # create dataframe for data
    X_win, X_loss = func(data)

    # create y variable for winning team (all 1's)
    oneGen = ((1 for x in range(X_win.shape[0])))
    Y_win = pd.DataFrame(oneGen, columns=['Win'])
    

    # create y variable for losing team (all 0's)
    zeroGen = ((0 for x in range(X_loss.shape[0])))
    Y_loss = pd.DataFrame(zeroGen, columns=['Win'])

    # concatenate wins and losses for analysis
    Y = pd.concat([Y_win, Y_loss], ignore_index=True)
    X = pd.concat([X_win, X_loss], ignore_index=True)

    # split data into training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=3)

    # scale and fix dimensions of each set
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    y_train = y_train.values.flatten()
    y_test = y_test.values.flatten()
    return X_train, X_test, y_train, y_test

# list of all modes
MODES = ('base', 'mp', 'pm', 'mpm', 'all')
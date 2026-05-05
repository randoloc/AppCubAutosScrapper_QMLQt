#include "vehiclemodel.h"
#include <QJsonArray>
#include <QJsonObject>
#include <QJsonDocument>

VehicleModel::VehicleModel(QObject *parent) : QAbstractListModel(parent) {}

int VehicleModel::rowCount(const QModelIndex &parent) const {
    if (parent.isValid()) return 0;
    return m_vehicles.size();
}

QVariant VehicleModel::data(const QModelIndex &index, int role) const {
    if (!index.isValid() || index.row() >= m_vehicles.size())
        return QVariant();

    const Vehicle &v = m_vehicles[index.row()];
    switch (role) {
        case TitleRole: return v.title;
        case PriceRole: return v.price > 0 ? v.price : QVariant();
        case CurrencyRole: return v.currency;
        case SourceLabelRole: return v.sourceLabel;
        case SourceRole: return v.source;
        case UrlRole: return v.url;
        case ProvinceRole: return v.province;
        case MunicipalityRole: return v.municipality;
        case ContactNameRole: return v.contactName;
        case ContactPhoneRole: return v.contactPhone;
        case ContactWhatsappRole: return v.contactWhatsapp;
        case DescriptionRole: return v.description;
        case AutonomiaKmRole: return v.autonomiaKm;
        case ModeloRole: return v.modelo;
        case BatteryKwhRole: return v.batteryKwh > 0 ? v.batteryKwh : QVariant();
        case ChargingTimeRole: return v.chargingTime;
        case ImagesRole: return v.images;
        case ImageUrlRole: return v.primaryImage;
        default: return QVariant();
    }
}

QHash<int, QByteArray> VehicleModel::roleNames() const {
    QHash<int, QByteArray> roles;
    roles[TitleRole] = "title";
    roles[PriceRole] = "price";
    roles[CurrencyRole] = "currency";
    roles[SourceLabelRole] = "sourceLabel";
    roles[SourceRole] = "source";
    roles[UrlRole] = "url";
    roles[ProvinceRole] = "province";
    roles[MunicipalityRole] = "municipality";
    roles[ContactNameRole] = "contactName";
    roles[ContactPhoneRole] = "contactPhone";
    roles[ContactWhatsappRole] = "contactWhatsapp";
    roles[DescriptionRole] = "description";
    roles[AutonomiaKmRole] = "autonomiaKm";
    roles[ModeloRole] = "modelo";
    roles[BatteryKwhRole] = "batteryKwh";
    roles[ChargingTimeRole] = "chargingTime";
    roles[ImagesRole] = "images";
    roles[ImageUrlRole] = "imageUrl";
    return roles;
}

void VehicleModel::clear() {
    beginResetModel();
    m_vehicles.clear();
    endResetModel();
}

QString VehicleModel::getImagesAsJson(int index) const {
    if (index < 0 || index >= m_vehicles.size()) return "[]";
    QJsonArray arr;
    for (const QString &img : m_vehicles[index].images) {
        arr.append(img);
    }
    return QString::fromUtf8(QJsonDocument(arr).toJson(QJsonDocument::Compact));
}

QVariantMap VehicleModel::get(int index) const {
    QVariantMap map;
    if (index < 0 || index >= m_vehicles.size()) return map;
    const Vehicle &v = m_vehicles[index];
    map["title"] = v.title;
    map["price"] = v.price;
    map["currency"] = v.currency;
    map["sourceLabel"] = v.sourceLabel;
    map["source"] = v.source;
    map["url"] = v.url;
    map["province"] = v.province;
    map["municipality"] = v.municipality;
    map["contactName"] = v.contactName;
    map["contactPhone"] = v.contactPhone;
    map["contactWhatsapp"] = v.contactWhatsapp;
    map["description"] = v.description;
    map["autonomiaKm"] = v.autonomiaKm;
    map["modelo"] = v.modelo;
    map["batteryKwh"] = v.batteryKwh;
    map["chargingTime"] = v.chargingTime;
    map["imageUrl"] = v.primaryImage;
    map["images"] = v.images;
    return map;
}

void VehicleModel::loadFromJson(const QJsonArray &array) {
    beginResetModel();
    m_vehicles.clear();

    for (const QJsonValue &val : array) {
        QJsonObject obj = val.toObject();
        Vehicle v;
        v.title = obj.value("title").toString();
        v.price = obj.value("price").toDouble();
        v.currency = obj.value("currency").toString();
        v.sourceLabel = obj.value("source_label").toString();
        v.source = obj.value("source").toString();
        v.url = obj.value("url").toString();
        v.province = obj.value("province").toString();
        v.municipality = obj.value("municipality").toString();
        v.contactName = obj.value("contact_name").toString();
        v.contactPhone = obj.value("contact_phone").toString();
        v.contactWhatsapp = obj.value("contact_whatsapp").toString();
        v.description = obj.value("description").toString();

        // Specs
        QJsonObject specs = obj.value("specs").toObject();
        if (!specs.isEmpty()) {
            v.autonomiaKm = specs.value("autonomia_km").toInt();
            v.modelo = specs.value("model").toString();
            if (v.modelo.isEmpty())
                v.modelo = specs.value("real_world_range").toString();
            v.batteryKwh = specs.value("battery_capacity_kwh").toDouble();
            v.chargingTime = specs.value("charging_time_10_80").toString();
        }

        // Images
        QJsonArray imgs = obj.value("images").toArray();
        for (const QJsonValue &img : imgs) {
            QString url = img.toString();
            if (!url.isEmpty()) {
                v.images.append(url);
            }
        }
        if (!v.images.isEmpty()) {
            v.primaryImage = v.images.first();
        }

        m_vehicles.append(v);
    }

    endResetModel();
}
